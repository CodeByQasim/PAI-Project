from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.project import Project

router = APIRouter()

@router.post("/projects")
def create_project(title: str, description: str = None, db: Session = Depends(get_db)):
    project = Project(title=title, description=description, user_id=1)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

@router.put("/projects/{project_id}")
def update_project(project_id: int, title: str = None, description: str = None, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if title:
        project.title = title
    if description:
        project.description = description
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
