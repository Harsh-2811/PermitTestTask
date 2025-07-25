import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Ensure the database directory exists
DB_DIR = "/app/db"  # Use absolute path in Docker
os.makedirs(DB_DIR, exist_ok=True)

# SQLite Database URL for Docker volume
DATABASE_URL = f"sqlite:///{DB_DIR}/permits.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
