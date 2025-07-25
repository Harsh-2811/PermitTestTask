from celery import Celery
from app.database import SessionLocal
from app.crud import PermitCRUD

celery = Celery(__name__, broker="redis://redis:6379/0")

@celery.task
def expire_pending_permits():
    db = SessionLocal()
    PermitCRUD().expire_old_permits(db)
    db.close()
