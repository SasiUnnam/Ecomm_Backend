from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.models.user import User
from app.routes.cart_routes import router as cart_router
from app.routes.order_routes import router as order_router
from app.utils.identifiers import format_user_id

# Include routers for testing without modifying main.py
if not any(getattr(r, "prefix", None) == "/orders" for r in app.routes):
    app.include_router(order_router)

if not any(getattr(r, "prefix", None) == "/carts" for r in app.routes):
    app.include_router(cart_router)


@pytest.fixture
def setup_user_and_product(client: TestClient, db_session):
    # 1. Create User
    user = User(
        first_name="Order",
        last_name="Tester",
        email="order_api_tester@example.com",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 2. Create Category & Subcategory
    category = Category(name="Order API Category", slug="order-api-cat")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    subcategory = SubCategory(
        category_id=category.id,
        name="Order API Subcategory",
        slug="order-api-subcat",
    )
    db_session.add(subcategory)
    db_session.commit()
    db_session.refresh(subcategory)

    # 3. Create Product
    product = Product(
        category_id=category.id,
        sub_category_id=subcategory.id,
        sku="SKU-ORDER-API-1",
        name="Order API Product",
        slug="order-api-product",
        price=Decimal("40.00"),
        status="active",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return user, product


def test_order_full_flow(client: TestClient, setup_user_and_product):
    user, product = setup_user_and_product
    formatted_user_id = format_user_id(user.id)

    # 1. Create Order with 1 item
    create_payload = {
        "user_id": formatted_user_id,
        "discount_amount": "5.00",
        "tax_amount": "3.50",
        "shipping_amount": "10.00",
        "items": [
            {
                "product_id": product.id,
                "quantity": 2,
            }
        ],
    }
    create_res = client.post("/orders", json=create_payload)
    assert create_res.status_code == 201
    order_data = create_res.json()
    order_id = order_data["id"]
    order_number = order_data["order_number"]

    assert order_data["user_id"] == formatted_user_id
    assert float(order_data["subtotal"]) == 80.00  # 40 * 2
    assert float(order_data["total_amount"]) == 88.50  # 80 - 5 + 3.5 + 10
    assert len(order_data["items"]) == 1
    assert order_data["items"][0]["product_name"] == "Order API Product"

    # 2. Get Order by ID
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == order_id

    # 3. Get Order by Order Number
    get_by_num = client.get(f"/orders/number/{order_number}")
    assert get_by_num.status_code == 200
    assert get_by_num.json()["id"] == order_id

    # 4. Get Orders by User
    user_orders_res = client.get(f"/orders/user/{formatted_user_id}")
    assert user_orders_res.status_code == 200
    assert len(user_orders_res.json()) >= 1

    # 5. List Orders with filter
    list_res = client.get("/orders", params={"status": "pending"})
    assert list_res.status_code == 200
    assert any(o["id"] == order_id for o in list_res.json())

    # 6. Update Order status
    patch_res = client.patch(
        f"/orders/{order_id}",
        json={"status": "placed"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "placed"
    assert patch_res.json()["placed_at"] is not None

    # 7. Add item to order
    add_item_res = client.post(
        f"/orders/{order_id}/items",
        json={"product_id": product.id, "quantity": 1},
    )
    assert add_item_res.status_code == 201
    item_id = add_item_res.json()["id"]
    assert float(add_item_res.json()["total_price"]) == 40.00

    # Verify order totals updated (80 + 40 = 120 subtotal)
    updated_order = client.get(f"/orders/{order_id}").json()
    assert float(updated_order["subtotal"]) == 120.00

    # 8. Get order items
    items_res = client.get(f"/orders/{order_id}/items")
    assert items_res.status_code == 200
    assert len(items_res.json()) == 2

    # 9. Get single order item
    single_item = client.get(f"/orders/{order_id}/items/{item_id}")
    assert single_item.status_code == 200
    assert single_item.json()["id"] == item_id

    # 10. Update order item quantity
    patch_item_res = client.patch(
        f"/orders/{order_id}/items/{item_id}",
        json={"quantity": 2},
    )
    assert patch_item_res.status_code == 200
    assert patch_item_res.json()["quantity"] == 2
    assert float(patch_item_res.json()["total_price"]) == 80.00

    # 11. Delete order item
    del_item_res = client.delete(f"/orders/{order_id}/items/{item_id}")
    assert del_item_res.status_code == 204

    # 12. Delete Order
    del_order_res = client.delete(f"/orders/{order_id}")
    assert del_order_res.status_code == 204

    # Verify 404
    assert client.get(f"/orders/{order_id}").status_code == 404


def test_order_from_cart_flow(client: TestClient, setup_user_and_product):
    user, product = setup_user_and_product
    formatted_user_id = format_user_id(user.id)

    # 1. Create cart
    cart_res = client.post("/carts", json={"user_id": formatted_user_id})
    assert cart_res.status_code == 201
    cart_id = cart_res.json()["id"]

    # 2. Add item to cart
    client.post(f"/carts/{cart_id}/items", json={"product_id": product.id, "quantity": 3})

    # 3. Create order from cart
    order_from_cart_res = client.post(f"/orders/from-cart/{formatted_user_id}")
    assert order_from_cart_res.status_code == 201
    order_data = order_from_cart_res.json()
    assert float(order_data["subtotal"]) == 120.00  # 40 * 3
    assert len(order_data["items"]) == 1

    # Verify cart is converted
    cart_check = client.get(f"/carts/{cart_id}").json()
    assert cart_check["status"] == "converted"


def test_order_errors(client: TestClient):
    # Non-existent order
    assert client.get("/orders/99999").status_code == 404
    assert client.get("/orders/number/NON-EXISTENT").status_code == 404

    # Adding item to non-existent order
    assert client.post("/orders/99999/items", json={"product_id": 1, "quantity": 1}).status_code == 404

    # Create order with invalid user
    assert (
        client.post(
            "/orders",
            json={"user_id": "00000000-0000-0000-0000-000000000000"},
        ).status_code
        == 404
    )
