import json
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..dto import Login
from ..models import User as UserSQLAlchemy
from ..database import get_db
from ..utils import hash, verify

router = APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def login(payload: Login, db: Session = Depends(get_db)):
    user = db.query(UserSQLAlchemy).filter(UserSQLAlchemy.email == payload.email).first()
    if not user:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=json.dumps({"data": f"user with email: {payload.email} not found"}),
            media_type="application/json"
        )
    elif not verify(payload.password, user.password): # hash(payload.password) != user.password
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"data": "password does not match"}),
            media_type="application/json"
        )
    
    # create and return token
    return Response(
        content=json.dumps({"data": {"token": "test_token"}}),
        media_type="application/json"
    )
