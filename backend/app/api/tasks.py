from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Import our database connection and our new DB model
from app.core.database import get_db
from app.models.task import DBTask

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    project_id: Optional[int] = None  # NEW: Optional field to link to a project

class TaskResponse(TaskCreate):
    id: int

    # This tells Pydantic to read the data even if it's not a standard Python dict
    # (i.e., it can read our SQLAlchemy DBTask object)
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks from Postgres."""
    tasks = db.query(DBTask).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by its ID."""
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task in Postgres."""
    # Convert Pydantic model to SQLAlchemy model
    new_task = DBTask(**task.model_dump()) 
    
    db.add(new_task)        # Add to session
    db.commit()             # Save to database
    db.refresh(new_task)    # Get the new ID assigned by Postgres
    
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Update an existing task."""
    existing_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields
    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.completed = task.completed
    
    db.commit()  # Save changes to database
    db.refresh(existing_task)  # Refresh to get updated data
    
    return existing_task


