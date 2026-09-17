from app.controllers import signup_controller


def test_auth_signup_request_otp_route(monkeypatch, client):
    async def fake_send_message(*args, **kwargs):
        return None

    monkeypatch.setattr(signup_controller.FastMail, "send_message", fake_send_message)

    response = client.post("/auth/signup/request-otp", json={"email": "route.user@example.com"})

    assert response.status_code == 202
    assert response.json()["message"] == "Verification code sent"


def test_auth_signup_verify_otp_route(client):
    email = "verify.route@example.com"
    otp = "654321"
    hashed = signup_controller.bcrypt.hashpw(otp.encode(), signup_controller.bcrypt.gensalt()).decode()
    signup_controller._pending_otps[email] = (
        hashed,
        signup_controller.datetime.now(signup_controller.timezone.utc) + signup_controller.timedelta(minutes=5),
    )

    response = client.post("/auth/signup/verify-otp", json={"email": email, "otp": otp})

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
