from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from users.auf import (
    hash_password,  
    verify_password,
    create_access_token,
    get_current_user,
)
from users.models import User
from users.shemas import (
    Token,
    UserCreate,
    UserRead,
)

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

@router.post(
    path="/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    new_user = User(
        username=user.username,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    path="/login",
    response_model=Token,
)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(db_user.username)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True
    )
    return {
        'access_token': token,
        'token_type': 'bearer',
    }

@router.get(
    path="/profile",
    response_model=UserRead,
)
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user