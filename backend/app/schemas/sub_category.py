from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.identifiers import format_subcategory_id


class SubCategoryBase(BaseModel):
    category_id: UUID
    name: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=180)
    description: str | None = None
    image_url: str | None = None
    is_active: bool = True


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(BaseModel):
    category_id: UUID | None = None
    name: str | None = Field(default=None, max_length=150)
    slug: str | None = Field(default=None, max_length=180)
    description: str | None = None
    image_url: str | None = None
    is_active: bool | None = None


class SubCategoryResponse(SubCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, subcategory_id: UUID) -> str:
        return format_subcategory_id(subcategory_id)