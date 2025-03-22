from typing import Dict, Optional, List
import numpy as np
from sentence_transformers import SentenceTransformer
from app.evaluators.base import BaseEvaluator
from app.models.models import Model, Prompt
from app.core.exceptions import EvaluationError

class FactualQAEvaluator(BaseEvaluator):
    """Evaluator for factual question-answering tasks."""
    
    def __init__(self, model: Model):
        super().__init__(model)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.metrics_list = [
            "semantic_similarity",
            "answer_presence",
            "contradiction_score"
        ]
    
    async def evaluate(self, prompt: Prompt) -> Dict[str, float]:
        """Run evaluation for factual QA."""
        if "expected_answer" not in prompt.metadata:
            raise EvaluationError("Prompt metadata must contain 'expected_answer'")
            
        completion = await self.get_completion(prompt)
        metrics = await self.calculate_metrics(completion, prompt.metadata["expected_answer"])
        return metrics
    
    async def validate_response(self, completion: str, expected: Optional[str] = None) -> bool:
        """Validate if the response contains a valid answer."""
        if not completion or not expected:
            return False
            
        similarity = self._calculate_similarity(completion, expected)
        return similarity > 0.7  # Threshold for valid response
    
    async def calculate_metrics(self, completion: str, expected: Optional[str] = None) -> Dict[str, float]:
        """Calculate evaluation metrics for factual QA."""
        if not expected:
            raise EvaluationError("Expected answer is required for factual QA evaluation")
            
        # Calculate semantic similarity
        similarity = self._calculate_similarity(completion, expected)
        self.add_metric("semantic_similarity", float(similarity))
        
        # Check for answer presence
        answer_presence = self._check_answer_presence(completion, expected)
        self.add_metric("answer_presence", float(answer_presence))
        
        # Calculate contradiction score (lower is better)
        contradiction = self._calculate_contradiction(completion, expected)
        self.add_metric("contradiction_score", float(contradiction))
        
        return self.get_metrics()
    
    async def get_completion(self, prompt: Prompt) -> str:
        """Get completion from the model."""
        # Implementation depends on model provider
        if self.model.provider == "openai":
            # Use OpenAI API
            from app.services.openai import get_completion
            return await get_completion(self.model, prompt.content)
        elif self.model.provider == "anthropic":
            # Use Anthropic API
            from app.services.anthropic import get_completion
            return await get_completion(self.model, prompt.content)
        else:
            raise EvaluationError(f"Unsupported model provider: {self.model.provider}")
    
    def get_supported_metrics(self) -> List[str]:
        """Get list of supported metrics."""
        return self.metrics_list
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        try:
            # Get embeddings
            emb1 = self.embedding_model.encode(text1, convert_to_tensor=True)
            emb2 = self.embedding_model.encode(text2, convert_to_tensor=True)
            
            # Calculate cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(similarity)
        except Exception as e:
            raise EvaluationError(f"Error calculating similarity: {str(e)}")
    
    def _check_answer_presence(self, completion: str, expected: str) -> float:
        """Check if key elements of the expected answer are present."""
        # Simple token overlap for now - could be enhanced with NER/keyword extraction
        completion_tokens = set(completion.lower().split())
        expected_tokens = set(expected.lower().split())
        overlap = len(completion_tokens.intersection(expected_tokens))
        return overlap / len(expected_tokens)
    
    def _calculate_contradiction(self, completion: str, expected: str) -> float:
        """Calculate a contradiction score between completion and expected answer."""
        # This is a simplified version - could be enhanced with NLI models
        similarity = self._calculate_similarity(completion, expected)
        return 1.0 - similarity  # Higher similarity = lower contradiction 