from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.signup_controller import request_signup_otp, verify_signup_otp
from app.schemas.user import SignupOTPRequest, SignupOTPVerify, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup/request-otp",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Email service unavailable or SMTP credentials invalid"
        }
    },
)
async def request_signup_code(
    data: SignupOTPRequest,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    await request_signup_otp(data, db)
    return {"message": "Verification code sent"}


@router.post(
    "/signup/verify-otp",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def verify_signup_code(
    data: SignupOTPVerify,
    db: Session = Depends(get_db),
) -> UserResponse:
    return await verify_signup_otp(data, db)