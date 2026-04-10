from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hostel Biometric Attendance"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"
    ALLOWED_SUBNET: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
