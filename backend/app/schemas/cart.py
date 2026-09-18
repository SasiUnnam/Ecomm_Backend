from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.identifiers import format_user_id


class CartBase(BaseModel):
    user_id: UUID
    status: Literal["active", "converted", "abandoned"] = "active"


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    status: Literal["active", "converted", "abandoned"] | None = None


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., max_digits=12, decimal_places=2)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


class CartItemResponse(CartItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CartResponse(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID) -> str:
        return format_user_id(user_id)
