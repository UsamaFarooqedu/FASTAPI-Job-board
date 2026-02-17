from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole, EmployeeProfile, CompanyProfile
from ..schemas import user as user_schema
from ..services import auth as auth_service
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=user_schema.User)
def register(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    hashed_password = auth_service.get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Initialize empty profiles
    if new_user.role == UserRole.EMPLOYEE:
        profile = EmployeeProfile(user_id=new_user.id, full_name="", headline="")
        db.add(profile)
    elif new_user.role == UserRole.COMPANY:
        profile = CompanyProfile(user_id=new_user.id, company_name=user_in.email.split('@')[0])
        db.add(profile)
    
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}
