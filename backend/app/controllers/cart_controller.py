from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartCreate, CartItemUpdate, CartUpdate


def get_carts(db: Session, skip: int = 0, limit: int = 100) -> list[Cart]:
    return db.query(Cart).offset(skip).limit(limit).all()


def get_cart(cart_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


def get_cart_by_user(user_id: UUID, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found for this user")
    return cart


def create_cart(cart_data: CartCreate, db: Session) -> Cart:
    user = db.query(User).filter(User.id == cart_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_cart = db.query(Cart).filter(Cart.user_id == cart_data.user_id).first()
    if existing_cart:
        raise HTTPException(status_code=400, detail="Cart already exists for this user")

    cart = Cart(
        user_id=cart_data.user_id,
        status=cart_data.status,
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def update_cart(cart_id: int, cart_data: CartUpdate, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    updates = cart_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(cart, field, value)

    db.commit()
    db.refresh(cart)
    return cart


def delete_cart(cart_id: int, db: Session) -> None:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.delete(cart)
    db.commit()


def clear_cart(cart_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.commit()
    db.refresh(cart)
    return cart


def get_cart_items(cart_id: int, db: Session) -> list[CartItem]:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


def get_cart_item(cart_id: int, item_id: int, db: Session) -> CartItem:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


def add_item_to_cart(
    cart_id: int,
    product_id: int,
    quantity: int,
    db: Session,
    unit_price: Decimal | None = None,
) -> CartItem:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if unit_price is None:
        unit_price = product.price

    existing_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        .first()
    )

    if existing_item:
        existing_item.quantity += quantity
        existing_item.unit_price = unit_price
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = CartItem(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_cart_item(
    cart_id: int,
    item_id: int,
    item_data: CartItemUpdate,
    db: Session,
) -> CartItem:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    updates = item_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def remove_item_from_cart(cart_id: int, item_id: int, db: Session) -> None:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
