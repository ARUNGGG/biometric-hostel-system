from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core.config import settings
from ipaddress import ip_address, ip_network

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        roll_number: str = payload.get("sub")
        if roll_number is None:
            raise credentials_exception
        token_data = schemas.TokenData(roll_number=roll_number)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Student).filter(models.Student.roll_number == token_data.roll_number).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user: models.Student = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

def verify_network(request: Request, db: Session = Depends(get_db)):
    client_host = request.client.host
    
    # Check if network is in allowed networks
    networks = db.query(models.AllowedNetwork).all()
    if not networks:
        # If no strict boundaries are defined yet, fail safe or allow. We'll strict fail if DB is set.
        pass
        
    is_allowed = False
    for net in networks:
        try:
            if ip_address(client_host) in ip_network(net.subnet):
                is_allowed = True
                break
        except ValueError:
            continue
            
    if not is_allowed and networks:
        raise HTTPException(status_code=403, detail="Network not allowed to mark attendance")
    
    return client_host
