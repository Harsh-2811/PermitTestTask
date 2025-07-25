from sqlalchemy.orm import Session
from app.models import Permit, PermitStatus
from app.schemas import PermitCreate
from datetime import datetime, timedelta

class PermitCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_permit(self, permit: PermitCreate):
        db_permit = Permit(**permit.dict())
        self.db.add(db_permit)
        self.db.commit()
        self.db.refresh(db_permit)
        return db_permit

    def get_permits(self, status: PermitStatus = None):
        query = self.db.query(Permit)
        if status:
            query = query.filter(Permit.status == status)
        return query.all()

    def update_permit_status(self, permit_id: int, status: PermitStatus):
        permit = self.db.query(Permit).filter(Permit.id == permit_id).first()
        if permit:
            permit.status = status
            self.db.commit()
            self.db.refresh(permit)
        return permit

    def expire_old_permits(self):
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        permits = self.db.query(Permit).filter(Permit.status == PermitStatus.pending, Permit.created_at < five_minutes_ago).all()
        for permit in permits:
            permit.status = PermitStatus.expired
            self.db.commit()
