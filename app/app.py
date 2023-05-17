import json
from fastapi import FastAPI, Response, status, Depends
from sqlalchemy.orm import Session
from .models import Post as PostSQLAlchemy
from .database import get_db, engine
from .dto import Post, PostUpdate

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
