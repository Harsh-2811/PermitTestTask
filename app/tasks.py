from worker.celery_worker import celery_app
import logging

from app.database import SessionLocal
from app.crud import PermitCRUD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def expire_pending_permits(self):
    db = SessionLocal()
    PermitCRUD(db).expire_old_permits()
    db.close()
