from typing import Any, Dict, Optional

class CustomException(Exception):
    def __init__(
        self,
        detail: str,
        status_code: int = 400,
        data: Optional[Dict[str, Any]] = None
    ):
        self.detail = detail
        self.status_code = status_code
        self.data = data or {}
        super().__init__(self.detail)

class ModelNotFoundError(CustomException):
    def __init__(self, model_id: str):
        super().__init__(
            detail=f"Model with ID {model_id} not found",
            status_code=404
        )

class EvaluationError(CustomException):
    def __init__(self, message: str):
        super().__init__(
            detail=f"Evaluation failed: {message}",
            status_code=500
        )

class InvalidPromptError(CustomException):
    def __init__(self, message: str):
        super().__init__(
            detail=f"Invalid prompt: {message}",
            status_code=400
        )

class APIKeyError(CustomException):
    def __init__(self, provider: str):
        super().__init__(
            detail=f"Missing or invalid API key for {provider}",
            status_code=401
        )

class RateLimitError(CustomException):
    def __init__(self, provider: str):
        super().__init__(
            detail=f"Rate limit exceeded for {provider}",
            status_code=429
        )

class DatabaseError(CustomException):
    def __init__(self, message: str):
        super().__init__(
            detail=f"Database error: {message}",
            status_code=500
        )

class AuthenticationError(CustomException):
    def __init__(self):
        super().__init__(
            detail="Could not validate credentials",
            status_code=401
        )

class PermissionError(CustomException):
    def __init__(self, resource: str):
        super().__init__(
            detail=f"Not enough permissions to access {resource}",
            status_code=403
        ) 