from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile as StarletteUploadFile

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
async def update_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> UserResponse:
    content_type = request.headers.get("content-type", "")
    image_data = None
    file_name = None
    image_content_type = None

    try:
        if content_type.startswith("multipart/form-data"):
            form = await request.form()
            form_data = {
                key: value
                for key, value in form.items()
                if not isinstance(value, StarletteUploadFile)
            }
            user_data = UserUpdate.model_validate(form_data)
            image_file = form.get("file")
            if isinstance(image_file, StarletteUploadFile):
                image_data = await image_file.read()
                file_name = image_file.filename
                image_content_type = image_file.content_type
        elif content_type.startswith("application/json"):
            user_data = UserUpdate.model_validate(await request.json())
        else:
            raise HTTPException(
                status_code=415,
                detail="Use application/json or multipart/form-data",
            )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    return update_user_controller(
        parse_user_id(user_id),
        user_data,
        db,
        image_data=image_data,
        file_name=file_name,
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
