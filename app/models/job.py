from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class EmploymentType(enum.Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    REMOTE = "Remote"

class ExperienceLevel(enum.Enum):
    ENTRY = "Entry"
    MID = "Mid"
    SENIOR = "Senior"
    LEAD = "Lead"
    EXECUTIVE = "Executive"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company_profiles.id"))
    title = Column(String, nullable=False)
    department = Column(String)
    employment_type = Column(Enum(EmploymentType), nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)
    location = Column(String)
    is_remote = Column(Boolean, default=False)
    description = Column(Text, nullable=False)
    responsibilities = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    benefits = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("CompanyProfile", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
