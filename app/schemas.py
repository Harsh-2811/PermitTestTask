from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class PermitStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    revoked = "revoked"
    expired = "expired"

class PermitCreate(BaseModel):
    name: str
    license_plate: str
    address: str

class PermitResponse(BaseModel):
    id: int
    name: str
    license_plate: str
    address: str
    status: PermitStatus
    created_at: datetime

    class Config:
        orm_mode = True
