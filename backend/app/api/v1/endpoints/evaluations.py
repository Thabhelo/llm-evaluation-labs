from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Evaluation, Model, Prompt, EvaluationType
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationResponse,
    EvaluationFilter,
    EvaluationBatchCreate
)
from app.evaluators.base import BaseEvaluator
from app.evaluators.factual_qa import FactualQAEvaluator
from app.core.celery_app import celery_app
from app.core.exceptions import EvaluationError, ModelNotFoundError

router = APIRouter()

# Evaluator factory
def get_evaluator(evaluation_type: EvaluationType, model: Model) -> BaseEvaluator:
    evaluators = {
        EvaluationType.FACTUAL_QA: FactualQAEvaluator,
        # Add other evaluator types here
    }
    
    evaluator_class = evaluators.get(evaluation_type)
    if not evaluator_class:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported evaluation type: {evaluation_type}"
        )
    
    return evaluator_class(model)

@router.post("/", response_model=EvaluationResponse)
async def create_evaluation(
    evaluation: EvaluationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new evaluation."""
    try:
        # Get model and prompt
        model = db.query(Model).filter(Model.id == evaluation.model_id).first()
        prompt = db.query(Prompt).filter(Prompt.id == evaluation.prompt_id).first()
        
        if not model or not prompt:
            raise ModelNotFoundError(evaluation.model_id)
            
        # Create evaluator
        evaluator = get_evaluator(prompt.type, model)
        
        # Create evaluation record
        db_evaluation = Evaluation(
            model_id=model.id,
            prompt_id=prompt.id,
            metadata=evaluation.metadata
        )
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)
        
        # Queue evaluation task
        task = celery_app.send_task(
            "app.evaluators.tasks.run_evaluation",
            args=[db_evaluation.id]
        )
        
        return {
            "id": db_evaluation.id,
            "status": "pending",
            "task_id": task.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/batch", response_model=List[EvaluationResponse])
async def create_batch_evaluation(
    batch: EvaluationBatchCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create multiple evaluations in batch."""
    responses = []
    
    for eval_create in batch.evaluations:
        try:
            response = await create_evaluation(eval_create, background_tasks, db)
            responses.append(response)
        except Exception as e:
            responses.append({
                "error": str(e),
                "model_id": eval_create.model_id,
                "prompt_id": eval_create.prompt_id
            })
    
    return responses

@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(evaluation_id: str, db: Session = Depends(get_db)):
    """Get evaluation by ID."""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.get("/", response_model=List[EvaluationResponse])
async def list_evaluations(
    filters: EvaluationFilter = Depends(),
    db: Session = Depends(get_db)
):
    """List evaluations with optional filtering."""
    query = db.query(Evaluation)
    
    if filters.model_id:
        query = query.filter(Evaluation.model_id == filters.model_id)
    if filters.prompt_id:
        query = query.filter(Evaluation.prompt_id == filters.prompt_id)
    if filters.evaluation_type:
        query = query.join(Prompt).filter(Prompt.type == filters.evaluation_type)
    
    evaluations = query.all()
    return evaluations

@router.delete("/{evaluation_id}")
async def delete_evaluation(evaluation_id: str, db: Session = Depends(get_db)):
    """Delete an evaluation."""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
        
    db.delete(evaluation)
    db.commit()
    return {"status": "success", "message": "Evaluation deleted"} 