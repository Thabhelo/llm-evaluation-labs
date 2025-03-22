import time
from typing import Dict, Any
from celery import Task
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.models import Evaluation, Model, Prompt, EvaluationType
from app.evaluators.base import BaseEvaluator
from app.evaluators.factual_qa import FactualQAEvaluator
from app.core.exceptions import EvaluationError
import logging

logger = logging.getLogger(__name__)

class SQLAlchemyTask(Task):
    """Base task that handles database sessions."""
    _db = None

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        """Close database session after task completion."""
        if self._db is not None:
            self._db.close()
            self._db = None

def get_evaluator(evaluation_type: EvaluationType, model: Model) -> BaseEvaluator:
    """Factory function to get the appropriate evaluator."""
    evaluators = {
        EvaluationType.FACTUAL_QA: FactualQAEvaluator,
        # Add other evaluator types here
    }
    
    evaluator_class = evaluators.get(evaluation_type)
    if not evaluator_class:
        raise EvaluationError(f"Unsupported evaluation type: {evaluation_type}")
    
    return evaluator_class(model)

@celery_app.task(base=SQLAlchemyTask, bind=True)
def run_evaluation(self, evaluation_id: str) -> Dict[str, Any]:
    """Run an evaluation asynchronously."""
    start_time = time.time()
    
    try:
        # Get evaluation record
        evaluation = self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if not evaluation:
            raise EvaluationError(f"Evaluation {evaluation_id} not found")
            
        # Get associated model and prompt
        model = self.db.query(Model).filter(Model.id == evaluation.model_id).first()
        prompt = self.db.query(Prompt).filter(Prompt.id == evaluation.prompt_id).first()
        
        if not model or not prompt:
            raise EvaluationError("Model or prompt not found")
            
        # Create evaluator
        evaluator = get_evaluator(prompt.type, model)
        
        # Run evaluation
        metrics = evaluator.evaluate(prompt)
        
        # Update evaluation record
        evaluation.scores = metrics
        evaluation.duration_ms = int((time.time() - start_time) * 1000)
        
        self.db.commit()
        
        return {
            "status": "success",
            "evaluation_id": evaluation_id,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
        
        if evaluation:
            evaluation.error = str(e)
            self.db.commit()
            
        return {
            "status": "error",
            "evaluation_id": evaluation_id,
            "error": str(e)
        }

@celery_app.task(base=SQLAlchemyTask, bind=True)
def run_batch_evaluation(self, evaluation_ids: list[str]) -> Dict[str, Any]:
    """Run multiple evaluations in batch."""
    results = []
    
    for eval_id in evaluation_ids:
        try:
            result = run_evaluation(eval_id)
            results.append(result)
        except Exception as e:
            results.append({
                "status": "error",
                "evaluation_id": eval_id,
                "error": str(e)
            })
    
    return {
        "status": "completed",
        "total": len(evaluation_ids),
        "results": results
    }

@celery_app.task(base=SQLAlchemyTask, bind=True)
def check_for_regressions(self, model_id: str, evaluation_type: EvaluationType) -> Dict[str, Any]:
    """Check for performance regressions in recent evaluations."""
    try:
        # Get recent evaluations for the model and type
        recent_evals = (
            self.db.query(Evaluation)
            .join(Prompt)
            .filter(
                Evaluation.model_id == model_id,
                Prompt.type == evaluation_type
            )
            .order_by(Evaluation.created_at.desc())
            .limit(100)
            .all()
        )
        
        if not recent_evals:
            return {"status": "no_data"}
            
        # Calculate average scores
        scores = [eval.scores for eval in recent_evals if eval.scores]
        if not scores:
            return {"status": "no_scores"}
            
        avg_scores = {}
        for metric in scores[0].keys():
            values = [s[metric] for s in scores if metric in s]
            avg_scores[metric] = sum(values) / len(values)
            
        # Compare with historical average
        historical_avg = {
            metric: sum(s[metric] for s in scores[10:] if metric in s) / len(scores[10:])
            for metric in scores[0].keys()
        }
        
        # Detect regressions
        regressions = {}
        for metric, current_avg in avg_scores.items():
            if metric in historical_avg:
                diff = current_avg - historical_avg[metric]
                if abs(diff) > 0.1:  # 10% threshold
                    regressions[metric] = {
                        "current": current_avg,
                        "historical": historical_avg[metric],
                        "difference": diff,
                        "severity": "high" if abs(diff) > 0.2 else "medium"
                    }
        
        return {
            "status": "success",
            "model_id": model_id,
            "evaluation_type": evaluation_type,
            "regressions": regressions,
            "sample_size": len(scores)
        }
        
    except Exception as e:
        logger.error(f"Regression check failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        } 