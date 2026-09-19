from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from pydantic import ValidationError
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


async def parse_user_update_payload(request: Request) -> UserUpdate:
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            payload = await request.json()
        except ValueError:
            payload = {}
        return UserUpdate(**(payload or {}))

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form_data = await request.form()
        payload = {
            "first_name": form_data.get("first_name"),
            "last_name": form_data.get("last_name"),
            "email": form_data.get("email"),
            "password": form_data.get("password"),
            "role": form_data.get("role"),
            "phone": form_data.get("phone"),
        }

        for key in ("is_active", "email_verified"):
            raw_value = form_data.get(key)
            if raw_value is not None:
                payload[key] = str(raw_value).lower() in {"true", "1", "yes", "on"}

        return UserUpdate(**{k: v for k, v in payload.items() if v is not None})

    return UserUpdate()


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> UserResponse:
    user_data = await parse_user_update_payload(request)
    return update_user_controller(
        parse_user_id(user_id),
        user_data,
        db,
    )


@router.patch("/{user_id}/form", response_model=UserResponse)
async def update_user_form(
    user_id: str,
    first_name: str | None = Form(default=None),
    last_name: str | None = Form(default=None),
    email: str | None = Form(default=None),
    phone: str | None = Form(default=None),
    is_active: bool | None = Form(default=None),
    email_verified: bool | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
) -> UserResponse:
    payload = UserUpdate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        is_active=is_active,
        email_verified=email_verified,
    )

    image_data = await file.read() if file is not None else None
    image_file_name = file.filename if file is not None else None
    image_content_type = file.content_type if file is not None else None

    return update_user_controller(
        parse_user_id(user_id),
        payload,
        db,
        image_data=image_data,
        file_name=image_file_name,
        content_type=image_content_type,
    )


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
