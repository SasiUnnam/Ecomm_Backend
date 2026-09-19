from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.order_controller import (
    add_item_to_order as add_item_to_order_controller,
    create_order as create_order_controller,
    create_order_from_cart as create_order_from_cart_controller,
    delete_order as delete_order_controller,
    get_order as get_order_controller,
    get_order_by_order_number as get_order_by_order_number_controller,
    get_order_item as get_order_item_controller,
    get_order_items as get_order_items_controller,
    get_orders as get_orders_controller,
    get_orders_by_user as get_orders_by_user_controller,
    remove_item_from_order as remove_item_from_order_controller,
    update_order as update_order_controller,
    update_order_item as update_order_item_controller,
)
from app.schemas.order import (
    OrderCreate,
    OrderItemCreate,
    OrderItemInput,
    OrderItemResponse,
    OrderItemUpdate,
    OrderResponse,
    OrderUpdate,
)
from app.utils.identifiers import parse_user_id

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderCreateRequest(BaseModel):
    user_id: str | UUID
    order_number: str | None = None
    shipping_address_id: int | None = None
    billing_address_id: int | None = None
    discount_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    tax_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    shipping_amount: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    status: str = "pending"
    payment_status: str = "pending"
    items: list[OrderItemInput] = Field(default_factory=list)


class OrderItemAddRequest(BaseModel):
    product_id: int
    product_name: str | None = None
    sku: str | None = None
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    total_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


@router.get("", response_model=list[OrderResponse])
def get_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    order_status: str | None = Query(default=None, alias="status"),
    payment_status: str | None = None,
    user_id: str | None = None,
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    parsed_user_id = parse_user_id(user_id) if user_id else None
    return get_orders_controller(
        db=db,
        skip=skip,
        limit=limit,
        status=order_status,
        payment_status=payment_status,
        user_id=parsed_user_id,
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreateRequest,
    db: Session = Depends(get_db),
) -> OrderResponse:
    user_id = parse_user_id(payload.user_id) if isinstance(payload.user_id, str) else payload.user_id
    order_data = OrderCreate(
        user_id=user_id,
        order_number=payload.order_number,
        shipping_address_id=payload.shipping_address_id,
        billing_address_id=payload.billing_address_id,
        discount_amount=payload.discount_amount,
        tax_amount=payload.tax_amount,
        shipping_amount=payload.shipping_amount,
        status=payload.status,
        payment_status=payload.payment_status,
        items=payload.items,
    )
    return create_order_controller(order_data=order_data, db=db)


@router.post("/from-cart/{user_id}", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    user_id: str,
    shipping_address_id: int | None = None,
    billing_address_id: int | None = None,
    db: Session = Depends(get_db),
) -> OrderResponse:
    parsed_id = parse_user_id(user_id)
    return create_order_from_cart_controller(
        user_id=parsed_id,
        db=db,
        shipping_address_id=shipping_address_id,
        billing_address_id=billing_address_id,
    )


@router.get("/number/{order_number}", response_model=OrderResponse)
def get_order_by_number(
    order_number: str,
    db: Session = Depends(get_db),
) -> OrderResponse:
    return get_order_by_order_number_controller(order_number=order_number, db=db)


@router.get("/user/{user_id}", response_model=list[OrderResponse])
def get_orders_by_user(
    user_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    parsed_id = parse_user_id(user_id)
    return get_orders_by_user_controller(user_id=parsed_id, db=db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
) -> OrderResponse:
    return get_order_controller(order_id=order_id, db=db)


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
) -> OrderResponse:
    return update_order_controller(order_id=order_id, order_data=order_data, db=db)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
) -> None:
    delete_order_controller(order_id=order_id, db=db)
    return None


@router.get("/{order_id}/items", response_model=list[OrderItemResponse])
def get_order_items(
    order_id: int,
    db: Session = Depends(get_db),
) -> list[OrderItemResponse]:
    return get_order_items_controller(order_id=order_id, db=db)


@router.post("/{order_id}/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_order(
    order_id: int,
    item_data: OrderItemAddRequest,
    db: Session = Depends(get_db),
) -> OrderItemResponse:
    order_item_create = OrderItemCreate(
        product_id=item_data.product_id,
        product_name=item_data.product_name,
        sku=item_data.sku,
        quantity=item_data.quantity,
        unit_price=item_data.unit_price,
        total_price=item_data.total_price,
    )
    return add_item_to_order_controller(
        order_id=order_id,
        item_data=order_item_create,
        db=db,
    )


@router.get("/{order_id}/items/{item_id}", response_model=OrderItemResponse)
def get_order_item(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
) -> OrderItemResponse:
    return get_order_item_controller(order_id=order_id, item_id=item_id, db=db)


@router.patch("/{order_id}/items/{item_id}", response_model=OrderItemResponse)
def update_order_item(
    order_id: int,
    item_id: int,
    item_data: OrderItemUpdate,
    db: Session = Depends(get_db),
) -> OrderItemResponse:
    return update_order_item_controller(
        order_id=order_id,
        item_id=item_id,
        item_data=item_data,
        db=db,
    )


@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_order(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
) -> None:
    remove_item_from_order_controller(order_id=order_id, item_id=item_id, db=db)
    return None
