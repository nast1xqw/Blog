from fastapi import APIRouter, Depends, Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from posts.models import Post
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from posts.models import Post
from posts.shemas import PostCreate

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / 'templates'

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(
    prefix = '/posts',
    tags = ['Page'] #группировка обработчиков в документации
)

@router.get('/')
async def list_posts_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse(request=request, name='posts/list.html', context={'posts': posts,})

@router.get('/create')
async def create_post_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='posts/create.html',
        context={}
    )

@router.post('/create')
async def create_post_submit(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    post = Post(title=title, content=content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return RedirectResponse(url='/posts/', status_code=303)

@router.get('/{post_id}')
async def get_post_page(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    return templates.TemplateResponse(
        request=request,
        name='posts/detail.html',
        context={'post': post}
    )