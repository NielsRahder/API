from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import posts, users, auth, vote
from .config import Settings

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True, 
    allow_methods=["*"],
    allow_headers=["*"]

)

#create the table in PGadmin
# models.base.metadata.create_all(bind = engine) #not necessary anymore bc of Alembic

#set up routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

#path operations 
@app.get("/") 
def root():
    return {"message": "Welkom op de API habibi"}

