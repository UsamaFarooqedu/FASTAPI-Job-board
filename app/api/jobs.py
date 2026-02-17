from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User, UserRole
from ..models.job import Job, EmploymentType, ExperienceLevel
from ..schemas import job as job_schema
from .users import get_current_user

router = APIRouter()

@router.post("/", response_model=job_schema.Job)
def create_job(
    job_in: job_schema.JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.COMPANY:
        raise HTTPException(status_code=403, detail="Only companies can post jobs")
    
    new_job = Job(
        **job_in.dict(),
        company_id=current_user.company_profile.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[job_schema.Job])
def list_jobs(
    skip: int = 0,
    limit: int = 20,
    q: Optional[str] = None,
    job_type: Optional[EmploymentType] = None,
    experience: Optional[ExperienceLevel] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.is_active == True)
    
    if q:
        query = query.filter(Job.title.contains(q) | Job.description.contains(q))
    if job_type:
        query = query.filter(Job.employment_type == job_type)
    if experience:
        query = query.filter(Job.experience_level == experience)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{job_id}", response_model=job_schema.Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=job_schema.Job)
def update_job(
    job_id: int,
    job_in: job_schema.JobUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.company_id != current_user.company_profile.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job")
    
    update_data = job_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job
