from fastapi import Depends
from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.signup_controller import request_signup_otp, verify_signup_otp
from app.controllers.user_controller import create_user as create_user_controller
from app.controllers.user_controller import get_user as get_user_controller
from app.controllers.user_controller import get_users as get_users_controller
from app.schemas.user import SignupOTPRequest, SignupOTPVerify, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup/request-otp", status_code=status.HTTP_202_ACCEPTED)
async def request_signup_code(data: SignupOTPRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    await request_signup_otp(data, db)
    return {"message": "Verification code sent"}


@router.post("/signup/verify-otp", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def verify_signup_code(data: SignupOTPVerify, db: Session = Depends(get_db)) -> UserResponse:
    return await verify_signup_otp(data, db)


@router.get("/")
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users_controller(db)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    return get_user_controller(user_id, db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return create_user_controller(user_data, db)
