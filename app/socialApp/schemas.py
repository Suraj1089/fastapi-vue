from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

class UpdatePost(Post):
    updated_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class UserOut(BaseModel):
    id: int 
    email: EmailStr 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 


class Token(BaseModel):
    acess_token: str 
    token_type: str 


class TokenData(BaseModel):
    id: Optional[int] = None 