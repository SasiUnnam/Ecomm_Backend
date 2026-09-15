import bcrypt

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


def get_users(db: Session) -> list[UserResponse]:
    return db.query(User).all()


def get_user(user_id: int, db: Session) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(user_data: UserCreate, db: Session) -> UserResponse:
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt()).decode(),
        role_id=user_data.role_id,
        phone=user_data.phone,
        is_active=user_data.is_active,
        email_verified=user_data.email_verified,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
