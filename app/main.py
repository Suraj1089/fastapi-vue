from fastapi import FastAPI
from .socialApp.database import engine,SessionLocal
from .socialApp.routers import posts,users,auth,chat 
from .socialApp import models
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(chat.router)


if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)




