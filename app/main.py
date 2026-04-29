from fastapi import FastAPI

from app.database import engine, Base   
from app import models
from app.routers import (
    users,
    auth,
    categories,
    articles,
    comments
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(articles.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"message": "Blog API Running Successfully"}