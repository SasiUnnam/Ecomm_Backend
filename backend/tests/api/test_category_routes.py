def test_create_category_route(client):
    payload = {"name": "Phones", "slug": "phones", "description": "Smartphones"}

    response = client.post("/categories", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["slug"] == "phones"
    assert data["name"] == "Phones"


def test_list_categories_route(client):
    client.post("/categories", json={"name": "Phones", "slug": "phones"})

    response = client.get("/categories")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(item["slug"] == "phones" for item in response.json())
