from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    category_id: UUID
    sub_category_id: UUID
    sku: str = Field(..., max_length=100)
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=280)
    description: str | None = None

    price: Decimal = Field(..., max_digits=12, decimal_places=2)
    compare_at_price: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
    )

    brand: str | None = Field(default=None, max_length=150)

    specifications: dict[str, Any] | None = None

    status: str = "active"
    is_featured: bool = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: UUID | None = None
    sub_category_id: UUID | None = None
    sku: str | None = Field(default=None, max_length=100)
    name: str | None = Field(default=None, max_length=255)
    slug: str | None = Field(default=None, max_length=280)
    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
    )

    compare_at_price: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
    )

    brand: str | None = Field(default=None, max_length=150)

    specifications: dict[str, Any] | None = None

    status: str | None = None
    is_featured: bool | None = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)