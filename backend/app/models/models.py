from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base
from uuid import uuid4

class ModelProvider(str, enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"

class EvaluationType(str, enum.Enum):
    FACTUAL_QA = "factual_qa"
    REASONING = "reasoning"
    CODING = "coding"
    MATH = "math"
    SAFETY = "safety"
    JAILBREAK = "jailbreak"
    AGENT = "agent"

class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    provider = Column(Enum(ModelProvider), nullable=False)
    version = Column(String)
    description = Column(Text)
    parameters = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    evaluations = relationship("Evaluation", back_populates="model")

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    content = Column(Text, nullable=False)
    type = Column(Enum(EvaluationType), nullable=False)
    tags = Column(JSON)  # Array of strings
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    evaluations = relationship("Evaluation", back_populates="prompt")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    model_id = Column(String, ForeignKey("models.id"), nullable=False)
    prompt_id = Column(String, ForeignKey("prompts.id"), nullable=False)
    completion = Column(Text, nullable=False)
    scores = Column(JSON)  # Dictionary of metric names to scores
    metadata = Column(JSON)
    error = Column(Text)
    duration_ms = Column(Integer)
    token_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("Model", back_populates="evaluations")
    prompt = relationship("Prompt", back_populates="evaluations")

class RegressionLog(Base):
    __tablename__ = "regression_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    model_id = Column(String, ForeignKey("models.id"), nullable=False)
    evaluation_type = Column(Enum(EvaluationType), nullable=False)
    previous_score = Column(Float)
    current_score = Column(Float)
    difference = Column(Float)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FailureCase(Base):
    __tablename__ = "failure_cases"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    evaluation_id = Column(String, ForeignKey("evaluations.id"), nullable=False)
    failure_type = Column(String, nullable=False)
    severity = Column(Integer)  # 1-5 scale
    description = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    evaluation = relationship("Evaluation") 