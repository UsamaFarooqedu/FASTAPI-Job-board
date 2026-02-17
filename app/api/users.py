from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole, EmployeeProfile, CompanyProfile
from ..schemas import user as user_schema
from ..services import auth as auth_service, file as file_service
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..config import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=user_schema.User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile/employee", response_model=user_schema.EmployeeProfile)
def update_employee_profile(
    profile_in: user_schema.EmployeeProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Not an employee account")
    
    profile = current_user.employee_profile
    for field, value in profile_in.dict().items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.put("/profile/company", response_model=user_schema.CompanyProfile)
def update_company_profile(
    profile_in: user_schema.CompanyProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.COMPANY:
        raise HTTPException(status_code=403, detail="Not a company account")
    
    profile = current_user.company_profile
    for field, value in profile_in.dict().items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/profile/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Not an employee account")
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_path = file_service.save_resume(file)
    current_user.employee_profile.resume_path = file_path
    db.commit()
    return {"path": file_path}
