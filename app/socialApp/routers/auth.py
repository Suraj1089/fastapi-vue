from fastapi import APIRouter,Depends,status,Response,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.socialApp.database import get_db
from app.socialApp import schemas,models,utils,oauth2


router = APIRouter(
    tags=['authentication']
)


@router.post('/login',response_model=schemas.Token)
def login(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==login_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    if not utils.verify_user(login_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    acess_token = oauth2.create_acess_token(data={'user_id':user.id})
    return {'acess_token':acess_token,"token_type": "bearer"}