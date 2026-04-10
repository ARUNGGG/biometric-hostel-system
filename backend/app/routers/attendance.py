from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
import json
from datetime import datetime, timedelta, timezone
from app import schemas, models
from app.database import get_db
from app.core import dependencies
from app.services import ml_service

router = APIRouter()

@router.post("/mark", response_model=schemas.AttendanceResponse)
def mark_attendance(
    request: Request,
    attendance_data: schemas.AttendanceMark,
    db: Session = Depends(get_db),
    current_user: models.Student = Depends(dependencies.get_current_user)
):
    # 1. Validate Network
    try:
        ip_address = dependencies.verify_network(request, db)
    except HTTPException as e:
        log = models.AttendanceLog(student_id=current_user.id, ip_address=request.client.host, status="failed_network")
        db.add(log)
        db.commit()
        raise e

    # 2. Rate Limiting / Duplicate Check
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=12)
    recent_log = db.query(models.AttendanceLog).filter(
        models.AttendanceLog.student_id == current_user.id,
        models.AttendanceLog.status == "success",
        models.AttendanceLog.timestamp >= time_threshold
    ).first()

    if recent_log:
        raise HTTPException(status_code=400, detail="Attendance already marked recently")

    # 3. Get User's stored embedding
    db_embedding = db.query(models.FaceEmbedding).filter(models.FaceEmbedding.student_id == current_user.id).first()
    if not db_embedding:
        raise HTTPException(status_code=400, detail="No face registered for this student")

    stored_vector = json.loads(db_embedding.embedding_vector)

    # 4. Extract face from incoming image and compare
    try:
        incoming_vector = ml_service.get_embedding(attendance_data.image_base64)
    except ValueError as e:
        log = models.AttendanceLog(student_id=current_user.id, ip_address=ip_address, status="failed_extraction")
        db.add(log)
        db.commit()
        raise HTTPException(status_code=400, detail=str(e))

    is_match, similarity = ml_service.is_match(stored_vector, incoming_vector)

    if not is_match:
        log = models.AttendanceLog(student_id=current_user.id, ip_address=ip_address, confidence_score=similarity, status="failed_match")
        db.add(log)
        db.commit()
        raise HTTPException(status_code=400, detail=f"Face verification failed. Confidence: {similarity:.2f}")

    # Success
    log = models.AttendanceLog(student_id=current_user.id, ip_address=ip_address, confidence_score=similarity, status="success")
    db.add(log)
    db.commit()
    return schemas.AttendanceResponse(status="success", confidence_score=similarity, message="Attendance marked successfully")
