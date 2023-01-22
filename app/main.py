from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
from fastapi import Response
from fastapi import status 
from fastapi import HTTPException
from .socialApp.database import engine,SessionLocal
from .socialApp import models,schemas
from sqlalchemy.orm import Session
from fastapi import Depends,Body

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.Posts,db:Session=Depends(get_db)):
    db_post = models.Posts(title=post.title,content=post.content,published=post.published,rating=post.rating)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts",status_code=status.HTTP_200_OK)
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts

@app.get("/posts/{id}",status_code=status.HTTP_200_OK)
def get_post(id:int,response:Response,db:Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not available")
    return post