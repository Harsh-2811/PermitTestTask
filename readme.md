# Permit Test Task

This project is a FastAPI application with Celery for background task processing.

## Prerequisites

- Python 3.8+
- Redis (for Celery broker)
- PostgreSQL (or any database supported by SQLAlchemy)
- `pip` for installing dependencies
- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PermitTestTask
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and configure the following:
   ```plaintext
   TOKEN=mocked_token
   ```

5. Start a Redis server (required for Celery):
   ```bash
   redis-server
   ```

## Running the FastAPI Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running the Celery Worker

1. Start the Celery worker:
   ```bash
   celery -A app.tasks worker --loglevel=info
   ```

2. Trigger the `expire_pending_permits` task manually (if needed):
   ```python
   from app.tasks import expire_pending_permits
   expire_pending_permits.delay()
   ```

## Running the Project with Docker

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the FastAPI application:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

3. The Celery worker will automatically start as part of the Docker Compose setup.

## Project Structure

```
PermitTestTask/
├── app/
│   ├── crud.py          # CRUD operations
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── routers.py       # API routes
│   ├── schemas.py       # Pydantic schemas
│   ├── tasks.py         # Celery tasks
│   ├── config.py        # Configuration settings
├── .env                 # Environment variables
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Dockerfile for FastAPI application
```