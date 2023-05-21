from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# DTO: Data Transfer Objects -> for request and response

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

class PostBase(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True

class Post(PostBase):
    # not pass user id when creating post, as the code will fetch from the JWT token
    pass

    class Config:
        orm_mode = True # convert to pydantic model from ORM model (SQLAlchemy)

class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]
    is_published: Optional[bool]

# limit the output content from the DB
class PostOut(PostBase):
    id: int
    is_published: bool
    created_at: datetime
    user_id: int
    user: UserOut
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str

class Register(Login):
    confirm_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
