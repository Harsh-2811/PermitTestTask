from app.tasks import celery

celery.conf.update(
    beat_schedule={
        "expire-pending-permits": {
            "task": "app.tasks.expire_pending_permits",
            "schedule": 60.0,
        },
    }
)

celery.start()
