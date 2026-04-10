from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import schemas, models
from app.database import get_db
from app.core import security, dependencies
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), client_ip: str = Depends(dependencies.verify_network)):
    user = db.query(models.Student).filter(models.Student.roll_number == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect roll number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.roll_number, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.Student)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Student).filter(models.Student.roll_number == student.roll_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Roll number already registered")
    
    db_email = db.query(models.Student).filter(models.Student.email == student.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(student.password)
    db_student = models.Student(
        name=student.name,
        roll_number=student.roll_number,
        email=student.email,
        password_hash=hashed_password,
        role=student.role
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/me", response_model=schemas.Student)
def read_users_me(current_user: models.Student = Depends(dependencies.get_current_user)):
    return current_user
