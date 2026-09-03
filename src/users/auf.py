import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwlib import PasswordHashe
from database import get_db
from models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "def-secret-key-change-me-32-bytes-min")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hashe = PasswordHash.recomended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/users/login",
)