from fastapi import APIRouter
from .endpoints import auth, models, evaluations, prompts, failures

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(failures.router, prefix="/failures", tags=["failures"]) 