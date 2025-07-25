from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base
import enum
import datetime

class PermitStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    revoked = "revoked"
    expired = "expired"

class Permit(Base):
    __tablename__ = "permits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_plate = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(Enum(PermitStatus), default=PermitStatus.pending)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
