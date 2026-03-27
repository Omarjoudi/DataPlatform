from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

fake_tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "description": "Build dummy endpoints", "completed": False},
    {"id": 2, "title": "Setup Postgres", "description": "Connect Neon or Supabase", "completed": False},
]

router = APIRouter()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@router.get("/", response_model=List[Task])
def get_all_tasks():
    """Retrieve all tasks."""
    return fake_tasks_db

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Retrieve a specific task by its ID."""
    for task in fake_tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=Task)
def create_task(task: Task):
    """Create a new task."""
    # Check if ID already exists to prevent duplicates in our DB
    if any(t["id"] == task.id for t in fake_tasks_db):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    
    fake_tasks_db.append(task.dict())
    return task


