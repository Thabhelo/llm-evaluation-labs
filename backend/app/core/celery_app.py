from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "llm_evaluation_lab",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Optional: Configure task routing
celery_app.conf.task_routes = {
    "app.evaluators.tasks.*": {"queue": "evaluations"},
    "app.core.tasks.*": {"queue": "default"},
} 