from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from ..models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[UserRole] = None

class EmployeeProfileBase(BaseModel):
    full_name: str
    headline: str
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None

class EmployeeProfileCreate(EmployeeProfileBase):
    pass

class EmployeeProfile(EmployeeProfileBase):
    id: int
    user_id: int
    profile_picture: Optional[str] = None
    resume_path: Optional[str] = None

    class Config:
        from_attributes = True

class CompanyProfileBase(BaseModel):
    company_name: str
    website: Optional[HttpUrl] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    description: Optional[str] = None

class CompanyProfileCreate(CompanyProfileBase):
    pass

class CompanyProfile(CompanyProfileBase):
    id: int
    user_id: int
    logo: Optional[str] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    employee_profile: Optional[EmployeeProfile] = None
    company_profile: Optional[CompanyProfile] = None

    class Config:
        from_attributes = True
