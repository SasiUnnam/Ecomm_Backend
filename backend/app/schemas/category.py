from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.identifiers import format_category_id


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=180)
    description: str | None = None
    image_url: str | None = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=150)
    slug: str | None = Field(default=None, max_length=180)
    description: str | None = None
    image_url: str | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, category_id: UUID) -> str:
        return format_category_id(category_id)