from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Shared properties
class StudentBase(BaseModel):
    name: str
    roll_number: str
    email: str
    role: Optional[str] = "student"

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    roll_number: Optional[str] = None

class AttendanceMark(BaseModel):
    image_base64: str

class AttendanceResponse(BaseModel):
    status: str
    confidence_score: Optional[float] = None
    message: str

class NetworkCreate(BaseModel):
    subnet: str
    description: Optional[str] = None
