from fastapi import FastAPI
from app.api import tasks, playing_with_neon
from app.core.database import engine, Base

# Import the models so SQLAlchemy knows about them before creating tables!
from app.models import task

# This line tells SQLAlchemy to build the tables in Postgres if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Web App API",
    description="Backend for the Dash frontend, powered by FastAPI",
    version="1.0.0"
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(playing_with_neon.router, prefix="/api/pwn", tags=["Pwn"])


@app.get("/")
def health_check():
    return {
        "status": "success", 
        "message": "FastAPI is connected and running!"
    }