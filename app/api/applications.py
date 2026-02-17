from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.job import Job
from ..models.application import Application, ApplicationStatus
from ..schemas import application as app_schema
from .users import get_current_user

router = APIRouter()

@router.post("/", response_model=app_schema.Application)
def apply_to_job(
    app_in: app_schema.ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Only employees can apply to jobs")
    
    # Check if already applied
    existing_app = db.query(Application).filter(
        Application.job_id == app_in.job_id,
        Application.employee_id == current_user.employee_profile.id
    ).first()
    
    if existing_app:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    # Check if resume exists
    if not current_user.employee_profile.resume_path:
        raise HTTPException(status_code=400, detail="Please upload a resume before applying")
    
    new_app = Application(
        job_id=app_in.job_id,
        employee_id=current_user.employee_profile.id,
        cover_letter=app_in.cover_letter,
        resume_path=current_user.employee_profile.resume_path
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.get("/my-applications", response_model=List[app_schema.Application])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Only employees can view their applications")
    
    return db.query(Application).filter(Application.employee_id == current_user.employee_profile.id).all()

@router.get("/job/{job_id}", response_model=List[app_schema.Application])
def get_job_applications(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or job.company_id != current_user.company_profile.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these applications")
    
    return db.query(Application).filter(Application.job_id == job_id).all()

@router.patch("/{app_id}/status", response_model=app_schema.Application)
def update_application_status(
    app_id: int,
    status_in: app_schema.ApplicationStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.job.company_id != current_user.company_profile.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this application")
    
    application.status = status_in.status
    db.commit()
    db.refresh(application)
    return application
