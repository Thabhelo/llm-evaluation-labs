from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from .config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Maximum number of connections in the pool
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=30,  # Timeout in seconds for getting a connection from the pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Enable connection health checks
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 