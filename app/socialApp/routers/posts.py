from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.socialApp.database import get_db
from app.socialApp import models,schemas,utils,oauth2


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

    
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    db_post = models.Post(**post.dict())     # unpack post dict
    print(user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/",status_code=status.HTTP_200_OK,response_model=list[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def get_post_id(id:int, db:Session=Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not available")
    return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id==id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found'
        )
    db.delete(posts)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.UpdatePost)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id==id)

    if not posts.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found'
        )
    posts.update(post.dict())
    db.commit()
    return posts.first()
    
