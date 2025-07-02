from .. import models, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from ..database import engine, get_db
from ..schema import PostBase, PostCreate, PostResponse, UserCreate, UserOut

router = APIRouter(
    prefix = "/users", 
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: session = Depends(get_db)):

    #hash the password - user.password
    
    hashed_password = utils.hash(user.password)
 
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 
    return new_user

@router.get("/{id}", status_code = status.HTTP_201_CREATED, response_model=UserOut)
def get_user(id:int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with {id} does not exist")
    return user 

