import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from database import get_db
from users.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "def-secret-key-change-me-32-bytes-min")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hashe = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/users/login",
)

def hash_password(password: str):
    return password_hashe.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hashe.verify(password, hashed_password)  

def create_access_token(username:str):
    payload = {
        'sub': username,
        'exp':(
            datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
    }  

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user =  db.query(User).filter(User.username==username,).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user