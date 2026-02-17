from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.job import EmploymentType, ExperienceLevel
from .user import CompanyProfile

class JobBase(BaseModel):
    title: str
    department: Optional[str] = None
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    location: Optional[str] = None
    is_remote: bool = False
    description: str
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "USD"
    benefits: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    title: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    experience_level: Optional[ExperienceLevel] = None
    description: Optional[str] = None

class Job(JobBase):
    id: int
    company_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company: CompanyProfile

    class Config:
        from_attributes = True
