from celery import Celery
from celery.schedules import crontab
import os

# Redis URL (adjust as needed)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Create Celery instance
celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Task routing
    task_routes={
        "tasks.send_email": {"queue": "emails"},
        "tasks.process_data": {"queue": "data_processing"},
    },
    # Beat schedule for periodic tasks
    beat_schedule={
        "daily-report": {
            "task": "app.tasks.expire_pending_permits",
            "schedule": crontab(minute="*/1"),  # Every 1 minute
        },
    },
)