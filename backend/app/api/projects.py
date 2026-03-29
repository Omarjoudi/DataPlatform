from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.models.projects import DBProject

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True
class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True

@router.get("/", response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    """Retrieve all projects from Postgres."""
    projects = db.query(DBProject).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
	project = db.query(DBProject).filter(DBProject.id == project_id).first()
	if project is None : 
		raise HTTPException(status_code=404, detail="Project not found")
	return project

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project in Postgres."""
    new_project = DBProject(**project.model_dump())
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project by its ID."""
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()

    return {"detail": f"Project with id {project_id} deleted successfully"}

