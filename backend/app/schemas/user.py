from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer

from app.models.role import RoleName
from app.utils.identifiers import format_user_id


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    role: RoleName = RoleName.USER
    phone: str | None = None
    profile_pic_url: str | None = None
    is_active: bool = True
    email_verified: bool = False


class UserCreate(UserBase):
    password: str


class SignupOTPRequest(BaseModel):
    email: EmailStr


class SignupOTPVerify(BaseModel):
    email: EmailStr
    otp: str


class ProfileImageUpload(BaseModel):
    image_data: str
    file_name: str | None = None
    content_type: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: RoleName | None = None
    phone: str | None = None
    profile_pic_url: str | None = None
    profile_image_data: str | None = None
    profile_image_name: str | None = None
    profile_image_content_type: str | None = None
    is_active: bool | None = None
    email_verified: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("id")
    def serialize_id(self, user_id: UUID) -> str:
        return format_user_id(user_id)


class UserInDB(UserResponse):
    password_hash: str | None = None