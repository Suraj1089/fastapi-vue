from sqlalchemy import Integer,String, Column,DateTime,Boolean,TIMESTAMP,ForeignKey
from .database import Base
from datetime import datetime
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean,server_default='TRUE')
    rating = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),onupdate=func.now())
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True,nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())