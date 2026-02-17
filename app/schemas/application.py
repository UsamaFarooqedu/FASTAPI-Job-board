from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.application import ApplicationStatus
from .user import EmployeeProfile

class ApplicationBase(BaseModel):
    cover_letter: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    job_id: int

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus

class Application(ApplicationBase):
    id: int
    job_id: int
    employee_id: int
    resume_path: str
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime
    employee: EmployeeProfile

    class Config:
        from_attributes = True
