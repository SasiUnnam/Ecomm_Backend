from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.identifiers import format_user_id


class OrderItemBase(BaseModel):
    product_id: int
    product_name: str = Field(..., max_length=255)
    sku: str | None = Field(default=None, max_length=100)
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., max_digits=12, decimal_places=2)
    total_price: Decimal = Field(..., max_digits=12, decimal_places=2)


class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str | None = Field(default=None, max_length=255)
    sku: str | None = Field(default=None, max_length=100)
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    total_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


class OrderItemInput(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


class OrderItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    total_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    user_id: UUID
    order_number: str | None = Field(default=None, max_length=50)
    shipping_address_id: int | None = None
    billing_address_id: int | None = None
    subtotal: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    tax_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    shipping_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    total_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    status: str = Field(default="pending", max_length=40)
    payment_status: str = Field(default="pending", max_length=40)
    placed_at: datetime | None = None


class OrderCreate(BaseModel):
    user_id: UUID
    order_number: str | None = Field(default=None, max_length=50)
    shipping_address_id: int | None = None
    billing_address_id: int | None = None
    discount_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    tax_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    shipping_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    subtotal: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    total_amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    status: str = Field(default="pending", max_length=40)
    payment_status: str = Field(default="pending", max_length=40)
    placed_at: datetime | None = None
    items: list[OrderItemInput] = Field(default_factory=list)


class OrderUpdate(BaseModel):
    shipping_address_id: int | None = None
    billing_address_id: int | None = None
    subtotal: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    discount_amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    tax_amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    shipping_amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    total_amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    status: str | None = Field(default=None, max_length=40)
    payment_status: str | None = Field(default=None, max_length=40)
    placed_at: datetime | None = None


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., max_length=40)


class OrderPaymentStatusUpdate(BaseModel):
    payment_status: str = Field(..., max_length=40)


class OrderResponse(OrderBase):
    id: int
    order_number: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id: UUID) -> str:
        return format_user_id(user_id)
