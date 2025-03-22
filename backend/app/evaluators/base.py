from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.models.models import Model, Prompt, Evaluation
from app.core.exceptions import EvaluationError

class BaseEvaluator(ABC):
    """Base class for all evaluators."""
    
    def __init__(self, model: Model):
        self.model = model
        self.metrics: Dict[str, float] = {}
        
    @abstractmethod
    async def evaluate(self, prompt: Prompt) -> Dict[str, float]:
        """
        Evaluate the model's response to a prompt.
        Returns a dictionary of metric names to scores.
        """
        pass
    
    @abstractmethod
    async def validate_response(self, completion: str, expected: Optional[str] = None) -> bool:
        """
        Validate if the model's response meets the evaluation criteria.
        """
        pass
    
    @abstractmethod
    async def calculate_metrics(self, completion: str, expected: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate evaluation metrics for the model's response.
        """
        pass
    
    async def run_evaluation(self, prompt: Prompt) -> Evaluation:
        """
        Run a complete evaluation cycle and return an Evaluation object.
        """
        try:
            # Get model completion
            completion = await self.get_completion(prompt)
            
            # Calculate metrics
            metrics = await self.calculate_metrics(completion)
            
            # Create evaluation record
            evaluation = Evaluation(
                model_id=self.model.id,
                prompt_id=prompt.id,
                completion=completion,
                scores=metrics,
                metadata={
                    "evaluator": self.__class__.__name__,
                    "model_parameters": self.model.parameters
                }
            )
            
            return evaluation
            
        except Exception as e:
            raise EvaluationError(str(e))
    
    @abstractmethod
    async def get_completion(self, prompt: Prompt) -> str:
        """
        Get completion from the model for a given prompt.
        """
        pass
    
    def add_metric(self, name: str, value: float) -> None:
        """
        Add a metric to the evaluator's metrics dictionary.
        """
        self.metrics[name] = value
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get all calculated metrics.
        """
        return self.metrics
    
    @abstractmethod
    def get_supported_metrics(self) -> List[str]:
        """
        Get list of metrics supported by this evaluator.
        """
        pass 