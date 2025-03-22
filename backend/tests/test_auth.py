from fastapi.testclient import TestClient
from typing import Dict

def test_login_success(client: TestClient, test_user: Dict[str, str]):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_user: Dict[str, str]):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user["email"],
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_wrong_email(client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "wrong@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_register_success(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "password": "newpassword",
            "full_name": "New User",
        },
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == "new@example.com"
    assert content["full_name"] == "New User"
    assert "id" in content
    assert not content["is_admin"]
    assert content["is_active"]

def test_register_existing_email(client: TestClient, test_user: Dict[str, str]):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user["email"],
            "password": "anotherpassword",
            "full_name": "Another User",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_current_user(client: TestClient, user_token: str):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert "email" in content
    assert "full_name" in content
    assert "id" in content

def test_get_current_user_no_token(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_current_user_wrong_token(client: TestClient):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer wrongtoken"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials" 