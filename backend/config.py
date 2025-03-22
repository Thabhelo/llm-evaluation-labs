from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "LLM Evaluation Labs"
    DEBUG: bool = False
    
    # Security
    JWT_SECRET_KEY: str = "your-secret-key-here"  # Change in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]  # Frontend URL
    
    # Database
    DATABASE_URL: str = "sqlite:///./llm_eval.db"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Model settings
    DEFAULT_MODEL: str = "gpt-4-turbo-preview"  # Default to GPT-4 Turbo
    FALLBACK_MODEL: str = "claude-3-opus-20240229"  # Fallback to Claude 3
    LOCAL_FALLBACK_MODEL: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Local fallback
    MAX_LOCAL_MODELS: int = 2
    
    # API Settings
    OPENAI_ORG_ID: Optional[str] = None
    OPENAI_API_VERSION: str = "2024-02-15"
    ANTHROPIC_API_VERSION: str = "2024-02-15"
    
    # Storage
    STORAGE_TYPE: str = "local"  # local or s3
    LOCAL_STORAGE_PATH: str = "./storage"
    
    # Cache
    CACHE_TYPE: str = "memory"  # memory or filesystem
    CACHE_DIR: str = "./cache"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"

settings = Settings() 