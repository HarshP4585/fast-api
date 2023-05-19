from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# DTO: Data Transfer Objects -> for request and response

class PostBase(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True

class Post(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]
    is_published: Optional[bool]

# limit the output content from the DB
class PostOut(PostBase):
    id: int
    is_published: bool
    created_at: str # datetime???

class UserBase(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str
