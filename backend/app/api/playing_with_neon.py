from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Import our database connection and our new DB model
from app.core.database import get_db
from app.models.playing_with_neon import DBPwn

router = APIRouter()

class TaskCreate(BaseModel):
    name: str
    value: float

class TaskResponse(TaskCreate):
    id: int

    # This tells Pydantic to read the data even if it's not a standard Python dict
    # (i.e., it can read our SQLAlchemy DBTask object)
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TaskResponse])
def get_all_pwn(db: Session = Depends(get_db)):
    """Retrieve all tasks from Postgres."""
    tasks = db.query(DBPwn).all()
    return tasks


@router.get("/{pwn_id}", response_model=TaskResponse)
def get_pwn(pwn_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by its ID."""
    task = db.query(DBPwn).filter(DBPwn.id == pwn_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse)
def create_pwn(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task in Postgres."""
    # Convert Pydantic model to SQLAlchemy model
    new_task = DBPwn(**task.model_dump()) 
    
    db.add(new_task)        # Add to session
    db.commit()             # Save to database
    db.refresh(new_task)    # Get the new ID assigned by Postgres
    
    return new_task

@router.delete("/{pwn_id}")
def delete_pwn(pwn_id: int, db: Session = Depends(get_db)):
    """Delete a specific task by its ID."""
    task = db.query(DBPwn).filter(DBPwn.id == pwn_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)  # Delete the task from the session
    db.commit()      # Commit the transaction to delete from database
    
    return {"detail": "Task deleted successfully"}


