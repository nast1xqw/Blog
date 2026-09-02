import uvicorn
from fastapi import FastAPI
from posts.routers import router as posts_api_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Blog',
)

app.include_router(posts_api_router)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8080,
        reload=True
    )