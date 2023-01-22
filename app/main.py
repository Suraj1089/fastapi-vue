from fastapi import FastAPI
from .socialApp.database import engine,SessionLocal
from .socialApp.routers import posts,users,auth
from .socialApp import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)





