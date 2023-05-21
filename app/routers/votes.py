import json
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import User as UserSQLAlchemy, Vote as VoteSQLAlchemy, Post as PostSQLAlchemy
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/vote-add/{id}")
def vote_add(id: int, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy] = Depends(get_current_user)):
    
    if not user:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "Not authorized to access the resource"}),
            media_type="application/json"
        )
    
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id).first()
    
    if not post:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=json.dumps({"data": f"post with id: {id} does not exits"}),
            media_type="application/json"
        )
    
    # if the user has already voted?
    post_vote = db.query(VoteSQLAlchemy).filter(VoteSQLAlchemy.post_id == id, VoteSQLAlchemy.user_id == user.id).first()
    
    if post_vote:
        return Response(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            content=json.dumps({"data": f"already liked post: {id}"}),
            media_type="application/json"
        )
    
    vote = VoteSQLAlchemy(post_id = id, user_id = user.id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"data": f"liked post: {id}"}),
        media_type="application/json"
    )

@router.post("/vote-remove/{id}")
def vote_remove(id: int, db: Session = Depends(get_db), user: Optional[UserSQLAlchemy] = Depends(get_current_user)):
    
    if not user:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "Not authorized to access the resource"}),
            media_type="application/json"
        )
    
    post = db.query(PostSQLAlchemy).filter(PostSQLAlchemy.id == id).first()
    
    if not post:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=json.dumps({"data": f"post with id: {id} does not exits"}),
            media_type="application/json"
        )
    
    # if the user has already voted?
    post_vote = db.query(VoteSQLAlchemy).filter(VoteSQLAlchemy.post_id == id, VoteSQLAlchemy.user_id == user.id)
    
    if not post_vote.first():
        return Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps({"data": f"no like on post: {id}"}),
            media_type="application/json"
        )
    
    post_vote.delete(synchronize_session=False)
    db.commit()
    
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
