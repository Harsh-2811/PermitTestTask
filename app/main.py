from fastapi import FastAPI
from app.database import Base, engine
from app.routers import router

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/heath_check")
def read_root():
    return {"message": "Welcome to the Permit Management API"}


# Include permit routes
app.include_router(router, prefix="/permits", tags=["permits"])
