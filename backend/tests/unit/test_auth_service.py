import asyncio
from datetime import datetime, timedelta, timezone

import bcrypt

from app.controllers.signup_controller import _pending_otps, request_signup_otp, verify_signup_otp
from app.schemas.user import SignupOTPRequest, SignupOTPVerify


def test_request_signup_otp_stores_pending_code(monkeypatch, db_session):
    email = "new.user@example.com"

    async def fake_send_message(*args, **kwargs):
        return None

    monkeypatch.setattr("app.controllers.signup_controller.FastMail.send_message", fake_send_message)

    asyncio.run(request_signup_otp(SignupOTPRequest(email=email), db_session))

    assert email in _pending_otps


def test_verify_signup_otp_creates_user(db_session):
    email = "verify.user@example.com"
    otp = "123456"
    hashed = bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()
    _pending_otps[email] = (hashed, datetime.now(timezone.utc) + timedelta(minutes=5))

    user = asyncio.run(verify_signup_otp(SignupOTPVerify(email=email, otp=otp), db_session))

    assert user.email == email
    assert user.email_verified is True
    assert email not in _pending_otps
