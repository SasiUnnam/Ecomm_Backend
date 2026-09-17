from app.utils.identifiers import parse_category_id, parse_subcategory_id


def test_create_product_route(client):
    category_response = client.post("/categories", json={"name": "Electronics", "slug": "electronics"})
    category_id = str(parse_category_id(category_response.json()["id"]))
    subcategory_response = client.post(
        "/subcategories",
        json={"category_id": category_id, "name": "Phones", "slug": "phones", "description": "Mobile phones"},
    )
    subcategory_id = str(parse_subcategory_id(subcategory_response.json()["id"]))

    payload = {
        "category_id": category_id,
        "sub_category_id": subcategory_id,
        "sku": "SKU-API-001",
        "name": "iPhone 15",
        "slug": "iphone-15",
        "description": "Latest iPhone",
        "price": "999.99",
        "compare_at_price": "1099.99",
        "brand": "Apple",
        "specifications": {"color": "blue"},
        "status": "active",
        "is_featured": True,
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "SKU-API-001"
    assert data["name"] == "iPhone 15"


def test_list_products_route(client):
    category_response = client.post("/categories", json={"name": "Electronics", "slug": "electronics"})
    category_id = str(parse_category_id(category_response.json()["id"]))
    subcategory_response = client.post(
        "/subcategories",
        json={"category_id": category_id, "name": "Phones", "slug": "phones"},
    )
    subcategory_id = str(parse_subcategory_id(subcategory_response.json()["id"]))
    client.post(
        "/products",
        json={
            "category_id": category_id,
            "sub_category_id": subcategory_id,
            "sku": "SKU-API-002",
            "name": "Galaxy S24",
            "slug": "galaxy-s24",
            "description": "Samsung smartphone",
            "price": "899.99",
            "brand": "Samsung",
            "status": "active",
            "is_featured": False,
        },
    )

    response = client.get("/products")

    assert response.status_code == 200
    result = response.json()
    assert any(item["slug"] == "galaxy-s24" for item in result)
