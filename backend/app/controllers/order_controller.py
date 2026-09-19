from datetime import datetime, timezone
from decimal import Decimal
import uuid
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderItemCreate,
    OrderItemUpdate,
    OrderUpdate,
)


def _generate_order_number() -> str:
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    random_str = uuid.uuid4().hex[:6].upper()
    return f"ORD-{timestamp_str}-{random_str}"


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    payment_status: str | None = None,
    user_id: UUID | None = None,
) -> list[Order]:
    query = db.query(Order)
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    if status is not None:
        query = query.filter(Order.status == status)
    if payment_status is not None:
        query = query.filter(Order.payment_status == payment_status)
    return query.offset(skip).limit(limit).all()


def get_order(order_id: int, db: Session) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_order_by_order_number(order_number: str, db: Session) -> Order:
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_orders_by_user(user_id: UUID, db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_order(order_data: OrderCreate, db: Session) -> Order:
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_number = order_data.order_number
    if order_number:
        existing = db.query(Order).filter(Order.order_number == order_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Order number already exists")
    else:
        order_number = _generate_order_number()

    # Calculate item totals
    subtotal = Decimal("0.00")
    order_items_to_create = []

    for item_input in order_data.items:
        product = db.query(Product).filter(Product.id == item_input.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item_input.product_id} not found")

        unit_price = item_input.unit_price if item_input.unit_price is not None else product.price
        total_price = unit_price * item_input.quantity
        subtotal += total_price

        order_items_to_create.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "quantity": item_input.quantity,
                "unit_price": unit_price,
                "total_price": total_price,
            }
        )

    if order_data.subtotal is not None:
        subtotal = order_data.subtotal

    discount_amount = order_data.discount_amount or Decimal("0.00")
    tax_amount = order_data.tax_amount or Decimal("0.00")
    shipping_amount = order_data.shipping_amount or Decimal("0.00")

    if order_data.total_amount is not None:
        total_amount = order_data.total_amount
    else:
        total_amount = subtotal - discount_amount + tax_amount + shipping_amount

    placed_at = order_data.placed_at
    if placed_at is None and order_data.status == "placed":
        placed_at = datetime.now(timezone.utc)

    order = Order(
        order_number=order_number,
        user_id=order_data.user_id,
        shipping_address_id=order_data.shipping_address_id,
        billing_address_id=order_data.billing_address_id,
        subtotal=subtotal,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        shipping_amount=shipping_amount,
        total_amount=total_amount,
        status=order_data.status,
        payment_status=order_data.payment_status,
        placed_at=placed_at,
    )
    db.add(order)
    db.flush()

    for item_dict in order_items_to_create:
        item = OrderItem(
            order_id=order.id,
            product_id=item_dict["product_id"],
            product_name=item_dict["product_name"],
            sku=item_dict["sku"],
            quantity=item_dict["quantity"],
            unit_price=item_dict["unit_price"],
            total_price=item_dict["total_price"],
        )
        db.add(item)

    db.commit()
    db.refresh(order)
    return order


def update_order(order_id: int, order_data: OrderUpdate, db: Session) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    updates = order_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(order, field, value)

    if updates.get("status") == "placed" and order.placed_at is None:
        order.placed_at = datetime.now(timezone.utc)

    # Recalculate total_amount if pricing fields were updated without an explicit total_amount
    pricing_updated = any(k in updates for k in ("subtotal", "discount_amount", "tax_amount", "shipping_amount"))
    if pricing_updated and "total_amount" not in updates:
        order.total_amount = (
            order.subtotal - order.discount_amount + order.tax_amount + order.shipping_amount
        )

    db.commit()
    db.refresh(order)
    return order


def delete_order(order_id: int, db: Session) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()


def get_order_items(order_id: int, db: Session) -> list[OrderItem]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def get_order_item(order_id: int, item_id: int, db: Session) -> OrderItem:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item = (
        db.query(OrderItem)
        .filter(OrderItem.id == item_id, OrderItem.order_id == order_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item


def add_item_to_order(
    order_id: int,
    item_data: OrderItemCreate,
    db: Session,
) -> OrderItem:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_name = item_data.product_name or product.name
    sku = item_data.sku or product.sku
    unit_price = item_data.unit_price if item_data.unit_price is not None else product.price
    total_price = (
        item_data.total_price
        if item_data.total_price is not None
        else unit_price * item_data.quantity
    )

    new_item = OrderItem(
        order_id=order_id,
        product_id=item_data.product_id,
        product_name=product_name,
        sku=sku,
        quantity=item_data.quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
    db.add(new_item)

    order.subtotal += total_price
    order.total_amount = (
        order.subtotal - order.discount_amount + order.tax_amount + order.shipping_amount
    )

    db.commit()
    db.refresh(new_item)
    return new_item


def update_order_item(
    order_id: int,
    item_id: int,
    item_data: OrderItemUpdate,
    db: Session,
) -> OrderItem:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item = (
        db.query(OrderItem)
        .filter(OrderItem.id == item_id, OrderItem.order_id == order_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    old_total_price = item.total_price

    updates = item_data.model_dump(exclude_unset=True)
    new_quantity = updates.get("quantity", item.quantity)
    new_unit_price = updates.get("unit_price", item.unit_price)

    if "total_price" in updates:
        item.total_price = updates["total_price"]
    elif "quantity" in updates or "unit_price" in updates:
        item.total_price = new_quantity * new_unit_price

    for field, value in updates.items():
        if field != "total_price":
            setattr(item, field, value)

    delta = item.total_price - old_total_price
    order.subtotal += delta
    order.total_amount = (
        order.subtotal - order.discount_amount + order.tax_amount + order.shipping_amount
    )

    db.commit()
    db.refresh(item)
    return item


def remove_item_from_order(order_id: int, item_id: int, db: Session) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item = (
        db.query(OrderItem)
        .filter(OrderItem.id == item_id, OrderItem.order_id == order_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    order.subtotal -= item.total_price
    if order.subtotal < Decimal("0.00"):
        order.subtotal = Decimal("0.00")

    order.total_amount = (
        order.subtotal - order.discount_amount + order.tax_amount + order.shipping_amount
    )
    if order.total_amount < Decimal("0.00"):
        order.total_amount = Decimal("0.00")

    db.delete(item)
    db.commit()


def create_order_from_cart(
    user_id: UUID,
    db: Session,
    shipping_address_id: int | None = None,
    billing_address_id: int | None = None,
) -> Order:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found for this user")

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    from app.schemas.order import OrderItemInput

    items_input = [
        OrderItemInput(
            product_id=ci.product_id,
            quantity=ci.quantity,
            unit_price=ci.unit_price,
        )
        for ci in cart_items
    ]

    order_data = OrderCreate(
        user_id=user_id,
        shipping_address_id=shipping_address_id,
        billing_address_id=billing_address_id,
        items=items_input,
    )

    order = create_order(order_data=order_data, db=db)
    cart.status = "converted"
    db.commit()

    return order
