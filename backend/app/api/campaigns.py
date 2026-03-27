from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

fake_tasks_db = [
    {"id": 1, "title": "Campaign1", "description": "Build campaign1", "completed": False},
    {"id": 2, "title": "Campaign2", "description": "Build campaign2", "completed": False},
]

router = APIRouter()

class Campaign(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@router.get("/", response_model=List[Campaign])
def get_all_tasks():
    """Retrieve all tasks."""
    return fake_tasks_db

@router.get("/{task_id}", response_model=Campaign)
def get_task(task_id: int):
    """Retrieve a specific task by its ID."""
    for task in fake_tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=Campaign)
def create_task(task: Campaign):
    """Create a new task."""
    # Check if ID already exists to prevent duplicates in our DB
    if any(t["id"] == task.id for t in fake_tasks_db):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    
    fake_tasks_db.append(task.dict())
    return task


