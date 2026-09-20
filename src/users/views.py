from pathlib import Path
from fastapi import APIRouter, Request, Depends, Response, status, Form
from users.auf import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import get_db
from sqlalchemy.orm import Session
from users.models import User
from users.auf import get_current_user, create_access_token, verify_password

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / 'templates'

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(
    tags=['Users Pages']
)

@router.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/login.html"
    )

@router.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/register.html"
    )

@router.get('/profile')
async def profile_page(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="users/profile.html",
        context={"user": current_user}  
    )

@router.post('/login')
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user or not verify_password(password, db_user.password):
        return templates.TemplateResponse(
            request=request,
            name="users/login.html",
            context={"error": "Неверный логин или пароль"}
        )

    access_token = create_access_token(db_user.username)
    
    redirect_response = RedirectResponse(
        url="/profile", 
        status_code=status.HTTP_302_FOUND
    )
    
    redirect_response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True
    )
    
    return redirect_response

@router.get('/logout')
async def logout():
    response = RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response
