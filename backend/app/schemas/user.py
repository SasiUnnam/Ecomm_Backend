from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    role_id: int | None = None
    phone: str | None = None
    is_active: bool = True
    email_verified: bool = False


class UserCreate(UserBase):
    password: str


class SignupOTPRequest(BaseModel):
    email: EmailStr


class SignupOTPVerify(BaseModel):
    email: EmailStr
    otp: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role_id: int | None = None
    phone: str | None = None
    is_active: bool | None = None
    email_verified: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserInDB(UserResponse):
    password_hash: str | None = None