from fastapi import APIRouter
from app.api.v1.endpoints import evaluations, models, prompts, analytics

api_router = APIRouter()

api_router.include_router(
    evaluations.router,
    prefix="/evaluations",
    tags=["evaluations"]
)

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["models"]
)

api_router.include_router(
    prompts.router,
    prefix="/prompts",
    tags=["prompts"]
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["analytics"]
) 