import json
from fastapi import Response, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User as UserSQLAlchemy
from ..dto import User, UserOut
from ..utils import hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserOut)
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

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserSQLAlchemy).filter(UserSQLAlchemy.id == id).first()
    if user:
        # user_out = UserOut(**{k: v for k, v in user.__dict__.items() if not k.startswith("_")})
        user_out = UserOut.from_orm(user)
        return Response(
            content=json.dumps({"data": user_out.dict()}, default=str),
            media_type="application/json"
        )
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"user with id: {id} not found"}),
        media_type="application/json"
    )
