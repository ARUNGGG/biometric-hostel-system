from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app import models
from app.core import security

from app.routers import auth, attendance, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hostel Biometric Attendance System")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        admin_user = db.query(models.Student).filter(models.Student.roll_number == "admin").first()
        if not admin_user:
            hashed_pw = security.get_password_hash("admin")
            db.add(models.Student(name="System Admin", roll_number="admin", email="admin@hostel.com", password_hash=hashed_pw, role="admin"))
        
        net = db.query(models.AllowedNetwork).filter(models.AllowedNetwork.subnet == "127.0.0.0/8").first()
        if not net:
            db.add(models.AllowedNetwork(subnet="127.0.0.0/8", description="Localhost loopback"))
        
        net2 = db.query(models.AllowedNetwork).filter(models.AllowedNetwork.subnet == "::1/128").first()
        if not net2:
            db.add(models.AllowedNetwork(subnet="::1/128", description="IPv6 Localhost"))
        db.commit()
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["attendance"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Welcome to Hostel Biometric Attendance System API"}
