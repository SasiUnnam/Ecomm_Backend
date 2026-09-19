from decimal import Decimal
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.cart_controller import (
    add_item_to_cart as add_item_to_cart_controller,
    clear_cart as clear_cart_controller,
    create_cart as create_cart_controller,
    delete_cart as delete_cart_controller,
    get_cart as get_cart_controller,
    get_cart_by_user as get_cart_by_user_controller,
    get_cart_item as get_cart_item_controller,
    get_cart_items as get_cart_items_controller,
    get_carts as get_carts_controller,
    remove_item_from_cart as remove_item_from_cart_controller,
    update_cart as update_cart_controller,
    update_cart_item as update_cart_item_controller,
)
from app.schemas.cart import (
    CartCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
    CartUpdate,
)
from app.utils.identifiers import parse_user_id

router = APIRouter(prefix="/carts", tags=["carts"])


class CartCreateRequest(BaseModel):
    user_id: str | UUID
    status: Literal["active", "converted", "abandoned"] = "active"


class CartItemAddRequest(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)


@router.get("", response_model=list[CartResponse])
def get_carts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[CartResponse]:
    return get_carts_controller(db=db, skip=skip, limit=limit)


@router.post("", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_cart(
    payload: CartCreateRequest,
    db: Session = Depends(get_db),
) -> CartResponse:
    user_id = parse_user_id(payload.user_id) if isinstance(payload.user_id, str) else payload.user_id
    cart_data = CartCreate(user_id=user_id, status=payload.status)
    return create_cart_controller(cart_data=cart_data, db=db)


@router.get("/user/{user_id}", response_model=CartResponse)
def get_cart_by_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> CartResponse:
    parsed_id = parse_user_id(user_id)
    return get_cart_by_user_controller(user_id=parsed_id, db=db)


@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(
    cart_id: int,
    db: Session = Depends(get_db),
) -> CartResponse:
    return get_cart_controller(cart_id=cart_id, db=db)


@router.patch("/{cart_id}", response_model=CartResponse)
def update_cart(
    cart_id: int,
    cart_data: CartUpdate,
    db: Session = Depends(get_db),
) -> CartResponse:
    return update_cart_controller(cart_id=cart_id, cart_data=cart_data, db=db)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
) -> None:
    delete_cart_controller(cart_id=cart_id, db=db)
    return None


@router.post("/{cart_id}/clear", response_model=CartResponse)
def clear_cart(
    cart_id: int,
    db: Session = Depends(get_db),
) -> CartResponse:
    return clear_cart_controller(cart_id=cart_id, db=db)


@router.get("/{cart_id}/items", response_model=list[CartItemResponse])
def get_cart_items(
    cart_id: int,
    db: Session = Depends(get_db),
) -> list[CartItemResponse]:
    return get_cart_items_controller(cart_id=cart_id, db=db)


@router.post("/{cart_id}/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    cart_id: int,
    item_data: CartItemAddRequest,
    db: Session = Depends(get_db),
) -> CartItemResponse:
    return add_item_to_cart_controller(
        cart_id=cart_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        unit_price=item_data.unit_price,
        db=db,
    )


@router.get("/{cart_id}/items/{item_id}", response_model=CartItemResponse)
def get_cart_item(
    cart_id: int,
    item_id: int,
    db: Session = Depends(get_db),
) -> CartItemResponse:
    return get_cart_item_controller(cart_id=cart_id, item_id=item_id, db=db)


@router.patch("/{cart_id}/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_id: int,
    item_id: int,
    item_data: CartItemUpdate,
    db: Session = Depends(get_db),
) -> CartItemResponse:
    return update_cart_item_controller(
        cart_id=cart_id,
        item_id=item_id,
        item_data=item_data,
        db=db,
    )


@router.delete("/{cart_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    cart_id: int,
    item_id: int,
    db: Session = Depends(get_db),
) -> None:
    remove_item_from_cart_controller(cart_id=cart_id, item_id=item_id, db=db)
    return None
