from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from posts.shemas import PostCreate, PostRead
from posts.models import Post

router = APIRouter(
    prefix = '/api',
    tags = ['API'] #группировка обработчиков в документации
)

@router.get('/posts', response_model = list[PostRead])
async def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.post('/posts', response_model = PostRead)
async def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    post = Post(
        title = post_data.title,
        content = post_data.content,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get('/{post_id}', response_model=PostRead | None)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.id == post_id).first()

@router.delete('/{post_id}', status_code=204)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post