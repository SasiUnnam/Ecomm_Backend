from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.orm import Session

from app.configs.mail import mail_config
from app.models.user import User
from app.schemas.user import SignupOTPRequest, SignupOTPVerify, UserResponse
from app.utils.otp import generate_otp

OTP_EXPIRY_MINUTES = 10
_pending_otps: dict[str, tuple[str, datetime]] = {}


async def request_signup_otp(data: SignupOTPRequest, db: Session) -> None:
    email = str(data.email).lower()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)
    _pending_otps[email] = (bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode(), expires_at)

    message = MessageSchema(
        recipients=[email],
        subject="Verify your Ecomm Backend email",
        body=f"Your verification code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.",
        subtype=MessageType.plain,
    )
    await FastMail(mail_config).send_message(message)


async def verify_signup_otp(data: SignupOTPVerify, db: Session) -> UserResponse:
    email = str(data.email).lower()
    pending_otp = _pending_otps.get(email)
    if pending_otp is None:
        raise HTTPException(status_code=400, detail="No verification code found")

    hashed_otp, expires_at = pending_otp
    if datetime.now(timezone.utc) >= expires_at:
        _pending_otps.pop(email, None)
        raise HTTPException(status_code=400, detail="Verification code has expired")
    if not bcrypt.checkpw(data.otp.encode(), hashed_otp.encode()):
        raise HTTPException(status_code=400, detail="Invalid verification code")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        _pending_otps.pop(email, None)
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    user = User(email=email, email_verified=True, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    _pending_otps.pop(email, None)
    return user
