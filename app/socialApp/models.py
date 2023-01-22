from sqlalchemy import Integer,String, Column,DateTime,Boolean
from .database import Base
from datetime import datetime
from sqlalchemy.sql import func


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    rating = Column(Integer)