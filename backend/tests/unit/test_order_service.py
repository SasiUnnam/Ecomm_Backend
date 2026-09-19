from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.controllers.cart_controller import add_item_to_cart, create_cart
from app.controllers.order_controller import (
    add_item_to_order,
    create_order,
    create_order_from_cart,
    delete_order,
    get_order,
    get_order_by_order_number,
    get_order_item,
    get_order_items,
    get_orders,
    get_orders_by_user,
    remove_item_from_order,
    update_order,
    update_order_item,
)
from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.models.user import User
from app.schemas.cart import CartCreate
from app.schemas.order import (
    OrderCreate,
    OrderItemCreate,
    OrderItemInput,
    OrderItemUpdate,
    OrderUpdate,
)


@pytest.fixture
def order_test_context(db_session):
    # 1. Create User
    user = User(
        first_name="Order",
        last_name="Tester",
        email="order_tester@example.com",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 2. Category & Subcategory
    category = Category(name="Order Category", slug="order-category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    subcategory = SubCategory(
        category_id=category.id,
        name="Order Subcategory",
        slug="order-subcategory",
    )
    db_session.add(subcategory)
    db_session.commit()
    db_session.refresh(subcategory)

    # 3. Product
    product = Product(
        category_id=category.id,
        sub_category_id=subcategory.id,
        sku="SKU-ORDER-UNIT-1",
        name="Unit Test Product",
        slug="unit-test-product",
        price=Decimal("25.00"),
        status="active",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return user, product


def test_create_order_success(db_session, order_test_context):
    user, product = order_test_context
    order_data = OrderCreate(
        user_id=user.id,
        discount_amount=Decimal("5.00"),
        tax_amount=Decimal("2.50"),
        shipping_amount=Decimal("10.00"),
        items=[OrderItemInput(product_id=product.id, quantity=2)],
    )

    order = create_order(order_data=order_data, db=db_session)
    assert order.id is not None
    assert order.order_number.startswith("ORD-")
    assert order.user_id == user.id
    assert order.subtotal == Decimal("50.00")
    assert order.discount_amount == Decimal("5.00")
    assert order.tax_amount == Decimal("2.50")
    assert order.shipping_amount == Decimal("10.00")
    # total = 50 - 5 + 2.5 + 10 = 57.50
    assert order.total_amount == Decimal("57.50")
    assert len(order.items) == 1
    assert order.items[0].product_name == "Unit Test Product"
    assert order.items[0].sku == "SKU-ORDER-UNIT-1"
    assert order.items[0].unit_price == Decimal("25.00")
    assert order.items[0].total_price == Decimal("50.00")


def test_get_and_filter_orders(db_session, order_test_context):
    user, product = order_test_context
    order1 = create_order(
        order_data=OrderCreate(
            user_id=user.id,
            status="pending",
            items=[OrderItemInput(product_id=product.id, quantity=1)],
        ),
        db=db_session,
    )

    order_fetched = get_order(order_id=order1.id, db=db_session)
    assert order_fetched.id == order1.id

    by_number = get_order_by_order_number(order_number=order1.order_number, db=db_session)
    assert by_number.id == order1.id

    user_orders = get_orders_by_user(user_id=user.id, db=db_session)
    assert len(user_orders) >= 1

    pending_orders = get_orders(db=db_session, status="pending")
    assert any(o.id == order1.id for o in pending_orders)


def test_update_order(db_session, order_test_context):
    user, product = order_test_context
    order = create_order(
        order_data=OrderCreate(
            user_id=user.id,
            items=[OrderItemInput(product_id=product.id, quantity=1)],
        ),
        db=db_session,
    )

    updated = update_order(
        order_id=order.id,
        order_data=OrderUpdate(status="placed", discount_amount=Decimal("10.00")),
        db=db_session,
    )
    assert updated.status == "placed"
    assert updated.placed_at is not None
    assert updated.discount_amount == Decimal("10.00")
    # subtotal was 25, discount 10 -> total 15
    assert updated.total_amount == Decimal("15.00")


def test_order_items_management(db_session, order_test_context):
    user, product = order_test_context
    order = create_order(
        order_data=OrderCreate(user_id=user.id),
        db=db_session,
    )
    assert order.subtotal == Decimal("0.00")

    # Add item
    item = add_item_to_order(
        order_id=order.id,
        item_data=OrderItemCreate(product_id=product.id, quantity=3),
        db=db_session,
    )
    assert item.quantity == 3
    assert item.total_price == Decimal("75.00")
    assert order.subtotal == Decimal("75.00")

    # Get items
    items = get_order_items(order_id=order.id, db=db_session)
    assert len(items) == 1
    single = get_order_item(order_id=order.id, item_id=item.id, db=db_session)
    assert single.id == item.id

    # Update item quantity
    updated_item = update_order_item(
        order_id=order.id,
        item_id=item.id,
        item_data=OrderItemUpdate(quantity=1),
        db=db_session,
    )
    assert updated_item.quantity == 1
    assert updated_item.total_price == Decimal("25.00")
    assert order.subtotal == Decimal("25.00")

    # Remove item
    remove_item_from_order(order_id=order.id, item_id=item.id, db=db_session)
    assert len(get_order_items(order_id=order.id, db=db_session)) == 0
    assert order.subtotal == Decimal("0.00")


def test_create_order_from_cart(db_session, order_test_context):
    user, product = order_test_context
    cart = create_cart(CartCreate(user_id=user.id), db=db_session)
    add_item_to_cart(cart_id=cart.id, product_id=product.id, quantity=2, db=db_session)

    order = create_order_from_cart(user_id=user.id, db=db_session)
    assert order.subtotal == Decimal("50.00")
    assert cart.status == "converted"


def test_delete_order(db_session, order_test_context):
    user, product = order_test_context
    order = create_order(
        order_data=OrderCreate(
            user_id=user.id,
            items=[OrderItemInput(product_id=product.id, quantity=1)],
        ),
        db=db_session,
    )
    order_id = order.id
    delete_order(order_id=order_id, db=db_session)

    with pytest.raises(HTTPException) as exc:
        get_order(order_id=order_id, db=db_session)
    assert exc.value.status_code == 404
