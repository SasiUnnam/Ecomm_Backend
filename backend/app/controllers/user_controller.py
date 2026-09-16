import bcrypt
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.role import RoleName
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.storage import delete_file, upload_profile_image


def get_users(db: Session) -> list[UserResponse]:
    return db.query(User).all()


def get_user(user_id: UUID, db: Session) -> UserResponse:
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
        role=user_data.role,
        phone=user_data.phone,
        profile_pic_url=user_data.profile_pic_url,
        is_active=user_data.is_active,
        email_verified=user_data.email_verified,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(user_id: UUID, user_data: UserUpdate, db: Session) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user_data.model_dump(exclude_unset=True)
    if "email" in updates:
        updates["email"] = str(updates["email"]).lower()
        existing_user = (
            db.query(User)
            .filter(User.email == updates["email"], User.id != user_id)
            .first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="A user with this email already exists")

    password = updates.pop("password", None)
    if password is not None:
        user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    profile_image_data = updates.pop("profile_image_data", None)
    profile_image_name = updates.pop("profile_image_name", None)
    profile_image_content_type = updates.pop("profile_image_content_type", None)

    if profile_image_data:
        previous_profile_pic_url = user.profile_pic_url
        uploaded_url = upload_profile_image(
            user_id=user_id,
            image_data=profile_image_data,
            file_name=profile_image_name,
            content_type=profile_image_content_type,
        )
        user.profile_pic_url = uploaded_url
        if previous_profile_pic_url and previous_profile_pic_url != uploaded_url:
            delete_file(previous_profile_pic_url)
        updates.pop("profile_pic_url", None)

    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def upload_user_profile_image(
    user_id: UUID,
    image_data: bytes,
    file_name: str | None,
    content_type: str | None,
    db: Session,
) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    previous_profile_pic_url = user.profile_pic_url
    image_url = upload_profile_image(
        user_id=user_id,
        image_data=image_data,
        file_name=file_name,
        content_type=content_type,
    )
    user.profile_pic_url = image_url
    if previous_profile_pic_url and previous_profile_pic_url != image_url:
        delete_file(previous_profile_pic_url)
    db.commit()
    db.refresh(user)
    return user
