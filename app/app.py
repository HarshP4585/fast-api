import json
from fastapi import FastAPI, Response, status, Depends
from sqlalchemy.orm import Session
from . import models
from .models import Post as PostSQLAlchemy, User as UserSQLAlchemy
from .database import get_db, engine
from .dto import Post, PostUpdate, User, UserOut
from .utils import hash

app = FastAPI()

# Create Tables from Models
# models.Base.metadata.create_all(bind=engine)

# Dummy controller using ORM
# @app.get("/posts_ORM")
# def get_posts_using_sqlalchemy(db: Session = Depends(get_db)):
#     posts = db.query(PostSQLAlchemy).all()
#     print(posts)
#     return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostSQLAlchemy).all()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id).first()
    if post:
        return {"data": post}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@app.post("/posts")
def create_post(payload: Post, db: Session = Depends(get_db)):
    post = PostSQLAlchemy(**payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"data": post}, default=str),
        media_type="application/json"
    )

@app.patch("/posts/{id}")
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id)
    post_data = post.first()
    if post_data:
        to_update = {k: v for k, v in payload if v is not None}
        post.update(to_update, synchronize_session=False)
        db.commit()
        db.refresh(post_data)
        return {"data": post_data}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@app.post("/users", response_model=UserOut)
def create_user(payload: User, db: Session = Depends(get_db)):
    user = UserSQLAlchemy(**payload.dict())
    user.password = hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    user_out = UserOut(**{k: v for k, v in user.__dict__.items() if not k.startswith("_")})
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"data": user_out.dict()}, default=str),
        media_type="application/json"
    )

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserSQLAlchemy).filter(UserSQLAlchemy.id == id).first()
    if user:
        user_out = UserOut(**{k: v for k, v in user.__dict__.items() if not k.startswith("_")})
        return Response(
            content=json.dumps({"data": user_out.dict()}, default=str),
            media_type="application/json"
        )
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"user with id: {id} not found"}),
        media_type="application/json"
    )
