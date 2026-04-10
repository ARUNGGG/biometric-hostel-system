from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    roll_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="student") # student or admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    embeddings = relationship("FaceEmbedding", back_populates="student")
    attendance_logs = relationship("AttendanceLog", back_populates="student")

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    embedding_vector = Column(String) # JSON compressed array of embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="embeddings")

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(Float)
    ip_address = Column(String)
    status = Column(String) # success, failed_network, failed_face

    student = relationship("Student", back_populates="attendance_logs")

class AllowedNetwork(Base):
    __tablename__ = "allowed_networks"

    id = Column(Integer, primary_key=True, index=True)
    subnet = Column(String, unique=True)
    description = Column(String)
