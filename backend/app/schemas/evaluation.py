from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.models import EvaluationType
from uuid import UUID

class EvaluationBase(BaseModel):
    model_id: str
    prompt_id: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class EvaluationCreate(EvaluationBase):
    pass

class EvaluationBatchCreate(BaseModel):
    evaluations: List[EvaluationCreate]

class EvaluationResponse(EvaluationBase):
    id: str
    completion: Optional[str]
    scores: Optional[Dict[str, float]]
    error: Optional[str]
    duration_ms: Optional[int]
    token_count: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationFilter(BaseModel):
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    evaluation_type: Optional[EvaluationType] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class EvaluationMetrics(BaseModel):
    semantic_similarity: Optional[float]
    answer_presence: Optional[float]
    contradiction_score: Optional[float]
    safety_scores: Optional[Dict[str, float]]
    token_metrics: Optional[Dict[str, int]]
    
    class Config:
        from_attributes = True

class EvaluationStats(BaseModel):
    total_count: int
    success_rate: float
    average_duration_ms: float
    average_scores: Dict[str, float]
    evaluation_types: Dict[str, int]
    error_distribution: Dict[str, int]
    
    class Config:
        from_attributes = True

class RegressionReport(BaseModel):
    model_id: str
    evaluation_type: EvaluationType
    previous_score: float
    current_score: float
    difference: float
    severity: str  # "low", "medium", "high"
    created_at: datetime
    
    class Config:
        from_attributes = True 