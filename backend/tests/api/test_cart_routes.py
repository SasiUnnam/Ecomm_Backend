from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.product import Product
from app.models.user import User
from app.routes.cart_routes import router as cart_router
from app.utils.identifiers import format_user_id, parse_category_id, parse_subcategory_id

# Include cart_router for testing without modifying main.py
if not any(getattr(r, "prefix", None) == "/carts" for r in app.routes):
    app.include_router(cart_router)


@pytest.fixture
def setup_user_and_product(client: TestClient, db_session):
    # 1. Create User
    user = User(
        first_name="Cart",
        last_name="Tester",
        email="cart_tester@example.com",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 2. Create Category
    cat_res = client.post("/categories", json={"name": "Cart Category", "slug": "cart-category"})
    assert cat_res.status_code == 201
    cat_id = str(parse_category_id(cat_res.json()["id"]))

    # 3. Create Subcategory
    subcat_res = client.post(
        "/subcategories",
        json={"category_id": cat_id, "name": "Cart Subcategory", "slug": "cart-subcategory"},
    )
    assert subcat_res.status_code == 201
    subcat_id = str(parse_subcategory_id(subcat_res.json()["id"]))

    # 4. Create Product
    product = Product(
        category_id=cat_id,
        sub_category_id=subcat_id,
        sku="SKU-CART-TEST-1",
        name="Cart Test Product",
        slug="cart-test-product",
        price=Decimal("49.99"),
        status="active",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return user, product


def test_cart_full_flow(client: TestClient, setup_user_and_product):
    user, product = setup_user_and_product
    formatted_user_id = format_user_id(user.id)

    # 1. Create Cart
    create_res = client.post("/carts", json={"user_id": formatted_user_id, "status": "active"})
    assert create_res.status_code == 201
    cart_data = create_res.json()
    assert cart_data["status"] == "active"
    assert cart_data["user_id"] == formatted_user_id
    cart_id = cart_data["id"]

    # 2. Duplicate Cart creation should return 400
    dup_res = client.post("/carts", json={"user_id": formatted_user_id, "status": "active"})
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 3. Get Cart by cart_id
    get_res = client.get(f"/carts/{cart_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == cart_id

    # 4. Get Cart by user_id
    get_user_cart_res = client.get(f"/carts/user/{formatted_user_id}")
    assert get_user_cart_res.status_code == 200
    assert get_user_cart_res.json()["id"] == cart_id

    # 5. Add Item to Cart (without unit_price, should default to product.price)
    add_res = client.post(
        f"/carts/{cart_id}/items",
        json={"product_id": product.id, "quantity": 2},
    )
    assert add_res.status_code == 201
    item_data = add_res.json()
    assert item_data["product_id"] == product.id
    assert item_data["quantity"] == 2
    assert float(item_data["unit_price"]) == 49.99
    item_id = item_data["id"]

    # 6. Add same item again (quantity should increment: 2 + 3 = 5)
    add_again_res = client.post(
        f"/carts/{cart_id}/items",
        json={"product_id": product.id, "quantity": 3},
    )
    assert add_again_res.status_code == 201
    assert add_again_res.json()["quantity"] == 5

    # 7. List Cart Items
    items_res = client.get(f"/carts/{cart_id}/items")
    assert items_res.status_code == 200
    assert len(items_res.json()) == 1

    # 8. Get Single Cart Item
    single_item_res = client.get(f"/carts/{cart_id}/items/{item_id}")
    assert single_item_res.status_code == 200
    assert single_item_res.json()["id"] == item_id

    # 9. Update Cart Item (change quantity to 1)
    update_item_res = client.patch(
        f"/carts/{cart_id}/items/{item_id}",
        json={"quantity": 1},
    )
    assert update_item_res.status_code == 200
    assert update_item_res.json()["quantity"] == 1

    # 10. Update Cart status
    update_cart_res = client.patch(
        f"/carts/{cart_id}",
        json={"status": "converted"},
    )
    assert update_cart_res.status_code == 200
    assert update_cart_res.json()["status"] == "converted"

    # 11. Remove Item from Cart
    del_item_res = client.delete(f"/carts/{cart_id}/items/{item_id}")
    assert del_item_res.status_code == 204

    # Verify Cart is empty
    empty_items_res = client.get(f"/carts/{cart_id}/items")
    assert empty_items_res.status_code == 200
    assert len(empty_items_res.json()) == 0

    # 12. Add item again and test clear_cart
    client.post(f"/carts/{cart_id}/items", json={"product_id": product.id, "quantity": 1})
    clear_res = client.post(f"/carts/{cart_id}/clear")
    assert clear_res.status_code == 200
    assert len(clear_res.json()["items"]) == 0

    # 13. Delete Cart
    del_cart_res = client.delete(f"/carts/{cart_id}")
    assert del_cart_res.status_code == 204

    # 14. Verify Cart 404 after deletion
    get_after_del = client.get(f"/carts/{cart_id}")
    assert get_after_del.status_code == 404


def test_cart_errors(client: TestClient):
    # Non-existent cart
    assert client.get("/carts/99999").status_code == 404
    assert client.get("/carts/user/00000000-0000-0000-0000-000000000000").status_code == 404

    # Adding item to non-existent cart
    assert client.post("/carts/99999/items", json={"product_id": 1, "quantity": 1}).status_code == 404

    # Creating cart for non-existent user
    assert (
        client.post(
            "/carts",
            json={"user_id": "00000000-0000-0000-0000-000000000000", "status": "active"},
        ).status_code
        == 404
    )
