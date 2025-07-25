import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Permit, PermitStatus
from app.crud import PermitCRUD
from app.schemas import PermitCreate
from datetime import datetime, timedelta

# Setup in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_permit(db):
    permit_crud = PermitCRUD(db)
    permit_data = PermitCreate(name="Test Permit", status=PermitStatus.pending)
    permit = permit_crud.create_permit(permit_data)
    assert permit.name == "Test Permit"
    assert permit.status == PermitStatus.pending

def test_get_permits(db):
    permit_crud = PermitCRUD(db)
    permit_data = PermitCreate(name="Test Permit", status=PermitStatus.pending)
    permit_crud.create_permit(permit_data)
    permits = permit_crud.get_permits(PermitStatus.pending)
    assert len(permits) == 1
    assert permits[0].name == "Test Permit"

def test_update_permit_status(db):
    permit_crud = PermitCRUD(db)
    permit_data = PermitCreate(name="Test Permit", status=PermitStatus.pending)
    permit = permit_crud.create_permit(permit_data)
    updated_permit = permit_crud.update_permit_status(permit.id, PermitStatus.approved)
    assert updated_permit.status == PermitStatus.approved

def test_expire_old_permits(db):
    permit_crud = PermitCRUD(db)
    old_permit_data = PermitCreate(name="Old Permit", status=PermitStatus.pending)
    old_permit = permit_crud.create_permit(old_permit_data)
    old_permit.created_at = datetime.utcnow() - timedelta(minutes=10)
    db.commit()
    permit_crud.expire_old_permits()
    expired_permit = db.query(Permit).filter(Permit.id == old_permit.id).first()
    assert expired_permit.status == PermitStatus.expired

def test_get_permits_with_status_filter(db):
    permit_crud = PermitCRUD(db)
    permit_data_pending = PermitCreate(name="Pending Permit", status=PermitStatus.pending)
    permit_data_approved = PermitCreate(name="Approved Permit", status=PermitStatus.approved)
    permit_crud.create_permit(permit_data_pending)
    permit_crud.create_permit(permit_data_approved)

    permits_pending = permit_crud.get_permits(PermitStatus.pending)
    assert len(permits_pending) == 1
    assert permits_pending[0].name == "Pending Permit"

    permits_approved = permit_crud.get_permits(PermitStatus.approved)
    assert len(permits_approved) == 1
    assert permits_approved[0].name == "Approved Permit"
