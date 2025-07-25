from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing import Annotated


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int
    
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # class Config: 
    #     orm_mode = True #this configuration is not requered in our version 

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config: 
        orm_mode = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str | int] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1) #later try to work with Annotated

