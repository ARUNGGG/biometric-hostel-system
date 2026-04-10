from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from app import schemas, models
from app.database import get_db
from app.core import dependencies
from app.services import ml_service

router = APIRouter()

@router.get("/students", response_model=List[schemas.Student])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    return db.query(models.Student).offset(skip).limit(limit).all()

@router.post("/add-student", response_model=schemas.Student)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    from app.routers.auth import register_student
    return register_student(student, db)

@router.post("/add-embedding/{student_id}")
def add_embedding(student_id: int, image_data: schemas.AttendanceMark, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    try:
        vector = ml_service.get_embedding(image_data.image_base64)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    db.query(models.FaceEmbedding).filter(models.FaceEmbedding.student_id == student_id).delete()
    
    db_emb = models.FaceEmbedding(student_id=student.id, embedding_vector=json.dumps(vector))
    db.add(db_emb)
    db.commit()
    return {"message": "Embedding registered successfully"}

@router.post("/add-network", response_model=schemas.NetworkCreate)
def add_network(network: schemas.NetworkCreate, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    db_net = models.AllowedNetwork(subnet=network.subnet, description=network.description)
    db.add(db_net)
    db.commit()
    db.refresh(db_net)
    return db_net

@router.get("/attendance")
def get_attendance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    logs = db.query(models.AttendanceLog).offset(skip).limit(limit).all()
    return logs

@router.delete("/remove-student/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db), admin: models.Student = Depends(dependencies.get_current_admin)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    db.query(models.FaceEmbedding).filter(models.FaceEmbedding.student_id == student_id).delete()
    db.query(models.AttendanceLog).filter(models.AttendanceLog.student_id == student_id).delete()
    db.delete(student)
    db.commit()
    return {"message": "Student successfully removed"}
