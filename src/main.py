import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from posts.routers import router as posts_api_router
from posts.views import router as posts_page_router   
from database import Base, engine

BASE_DIR = Path(__file__).resolve().parents[1]       
STATIC_DIR = BASE_DIR / 'static'                      

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Blog')

app.include_router(posts_api_router)
app.include_router(posts_page_router)

app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)