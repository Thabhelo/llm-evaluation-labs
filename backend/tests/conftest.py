import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import Generator, Dict

from ..database import Base
from ..main import app
from ..auth.deps import get_db
from ..models.user import User
from ..auth.utils import get_password_hash, create_access_token

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db: TestingSessionLocal) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def test_user(db: TestingSessionLocal) -> Dict[str, str]:
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "password": "testpassword",
        "full_name": user.full_name,
    }

@pytest.fixture(scope="module")
def test_admin(db: TestingSessionLocal) -> Dict[str, str]:
    user = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "password": "adminpassword",
        "full_name": user.full_name,
    }

@pytest.fixture(scope="module")
def user_token(test_user: Dict[str, str]) -> str:
    return create_access_token(data={"sub": str(test_user["id"])})

@pytest.fixture(scope="module")
def admin_token(test_admin: Dict[str, str]) -> str:
    return create_access_token(data={"sub": str(test_admin["id"])}) 