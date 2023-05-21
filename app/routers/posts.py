import json
from typing import Optional, List
from fastapi import Response, Depends, status, APIRouter
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Post as PostSQLAlchemy, User as UserSQLAlchemy
from ..dto import Post, PostUpdate, PostOut
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Dummy controller using ORM
# @router.get("/posts_ORM")
# def get_posts_using_sqlalchemy(db: Session = Depends(get_db)):
#     posts = db.query(PostSQLAlchemy).all()
#     print(posts)
#     return {"data": posts}

@router.get("/")
def get_posts(db: Session = Depends(get_db),
            #   user: Optional[UserSQLAlchemy] = Depends(get_current_user)
              ):
    # get all users' posts
    posts = db.query(PostSQLAlchemy).all()
    
    # get current user's posts
    # posts = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.user_id == user.id).all()
    
    posts_out_pydantic = parse_obj_as(List[PostOut], posts)
    return {"data": posts_out_pydantic}

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id).first()
    if post:
        post_out = PostOut.from_orm(post)
        return {"data": post_out.dict()}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@router.post("/")
def create_post(payload: Post, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy] = Depends(get_current_user)):
    if not user:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "Not authorized to access the resource"}),
            media_type="application/json"
        )
    post = PostSQLAlchemy(user_id = user.id, **payload.dict())
    # post.user_id = user.id
    db.add(post)
    db.commit()
    db.refresh(post)
    post_dict = PostOut.from_orm(post).dict()
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"data": post_dict}, default=str),
        media_type="application/json"
    )

@router.patch("/{id}")
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy] = Depends(get_current_user)):
    
    if not user:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "Not authorized to access the resource"}),
            media_type="application/json"
        )
    
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id)
    post_data = post.first()
    
    if post_data.user_id != user.id:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"data": "Not allowed to delete other user's posts"}),
            media_type="application/json"
        )
    
    if post_data:
        to_update = {k: v for k, v in payload if v is not None}
        post.update(to_update, synchronize_session=False)
        db.commit()
        db.refresh(post_data)
        post_out = PostOut.from_orm(post_data)
        return {"data": post_out.dict()}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy] = Depends(get_current_user)):
    
    if not user:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "Not authorized to access the resource"}),
            media_type="application/json"
        )
    
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id)
    post_data = post.first()
    
    # let user only delete own posts
    if post_data.user_id != user.id:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content=json.dumps({"data": "Not allowed to delete other user's posts"}),
            media_type="application/json"
        )
    
    if post_data:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )
