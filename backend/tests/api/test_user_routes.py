def test_update_user_route_accepts_form_urlencoded(client):
    created = client.post(
        "/users",
        json={
            "first_name": "Alice",
            "last_name": "Tester",
            "email": "alice@example.com",
            "password": "StrongPass123!",
            "role": "user",
            "phone": "+1234567890",
        },
    )
    user_id = created.json()["id"]

    response = client.patch(
        f"/users/{user_id}",
        data={
            "first_name": "Alicia",
            "email": "alice.updated@example.com",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["first_name"] == "Alicia"
    assert payload["email"] == "alice.updated@example.com"
