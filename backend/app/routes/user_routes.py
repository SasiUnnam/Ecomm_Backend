from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.user_controller import create_user as create_user_controller
from app.controllers.user_controller import get_user as get_user_controller
from app.controllers.user_controller import get_users as get_users_controller
from app.controllers.user_controller import update_user as update_user_controller
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.identifiers import parse_user_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users_controller(db)


@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserResponse:
    return get_user_controller(parse_user_id(user_id), db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return create_user_controller(user_data, db)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    return update_user_controller(parse_user_id(user_id), user_data, db)


@router.post("/{user_id}/profile-image", response_model=UserResponse)
async def upload_user_profile_image(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UserResponse:
    file_bytes = await file.read()
    return update_user_controller(
        parse_user_id(user_id),
        UserUpdate(),
        db,
        image_data=file_bytes,
        file_name=file.filename,
        content_type=file.content_type,
    )
