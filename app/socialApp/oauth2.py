from datetime import datetime,timedelta
from jose import JWTError,jwt
from app.socialApp import schemas
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "69d25e094faa6ca2556c818366bra9563d93f7099f6f0f4caa6cf63b88e8d3e7"
ALOGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALOGORITH)
    return token


def verify_acess_token(token: str, credentials_excpetions):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALOGORITH)
        id = payload.get("user_id")
        if id is None:
            raise credentials_excpetions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_excpetions
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )

    return verify_acess_token(token,credentials_exception)
