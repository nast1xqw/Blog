import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from posts.routers import router as posts_api_router
from posts.views import router as posts_page_router   
from database import Base, engine
from users.routers import router as users_api_router
from users.views import router as users_page_router

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")                      

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Blog')

app.include_router(posts_api_router)
app.include_router(posts_page_router)
app.include_router(users_api_router)
app.include_router(users_page_router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)