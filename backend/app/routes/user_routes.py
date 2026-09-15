from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.configs.database import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/")
def create_user(full_name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(full_name=full_name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
