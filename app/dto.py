from pydantic import BaseModel
from typing import Optional

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
