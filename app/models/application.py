from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class ApplicationStatus(enum.Enum):
    PENDING = "Pending"
    REVIEWING = "Reviewing"
    SHORTLISTED = "Shortlisted"
    INTERVIEWED = "Interviewed"
    REJECTED = "Rejected"
    HIRED = "Hired"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    employee_id = Column(Integer, ForeignKey("employee_profiles.id"))
    cover_letter = Column(Text, nullable=True)
    resume_path = Column(String, nullable=False) # Snapshot of resume at application time
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="applications")
    employee = relationship("EmployeeProfile")
