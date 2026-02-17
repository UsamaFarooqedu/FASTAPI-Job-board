from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    COMPANY = "company"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee_profile = relationship("EmployeeProfile", back_populates="user", uselist=False)
    company_profile = relationship("CompanyProfile", back_populates="user", uselist=False)

class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    headline = Column(String)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String, nullable=True)
    resume_path = Column(String, nullable=True)
    skills = Column(Text, nullable=True) # Stored as comma-separated or JSON string
    
    user = relationship("User", back_populates="employee_profile")

class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String, unique=True)
    website = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo = Column(String, nullable=True)
    
    user = relationship("User", back_populates="company_profile")
    jobs = relationship("Job", back_populates="company")
