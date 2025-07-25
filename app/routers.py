from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import PermitCRUD
from app.schemas import PermitCreate
from app.models import PermitStatus
from app.database import get_db
from app.config import settings

def get_current_user(token: str = Query(..., description="Mock token for authentication")):
    if token != settings.TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return {"username": "mock_user"}

router = APIRouter()

@router.post("/permits/")
def create_permit(
    permit: PermitCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permit_crud = PermitCRUD(db)
    return permit_crud.create_permit(permit)

@router.get("/permits/")
def get_permits(
    status: str = Query(
        None, description="Filter permits by status"
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permit_crud = PermitCRUD(db)
    try:
        status_enum = PermitStatus[status] if status else None
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid status value")
    return permit_crud.get_permits(status_enum)

@router.put("/permits/{permit_id}/status/")
def update_permit_status(
    permit_id: int,
    status: PermitStatus,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permit_crud = PermitCRUD(db)
    permit = permit_crud.update_permit_status(permit_id, status)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit

@router.post("/permits/expire/")
def expire_old_permits(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permit_crud = PermitCRUD(db)
    permit_crud.expire_old_permits()
    return {"message": "Expired old permits successfully"}
