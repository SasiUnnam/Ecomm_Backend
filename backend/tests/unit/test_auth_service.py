import asyncio
from datetime import datetime, timedelta, timezone

import bcrypt
import pytest
from fastapi import HTTPException

from app.controllers.signup_controller import _pending_otps, request_signup_otp, verify_signup_otp
from app.schemas.user import SignupOTPRequest, SignupOTPVerify


def test_request_signup_otp_stores_pending_code(monkeypatch, db_session):
    email = "new.user@example.com"

    async def fake_send_message(*args, **kwargs):
        return None

    monkeypatch.setattr("app.controllers.signup_controller.FastMail.send_message", fake_send_message)

    asyncio.run(request_signup_otp(SignupOTPRequest(email=email), db_session))

    assert email in _pending_otps


def test_request_signup_otp_handles_email_send_failure(monkeypatch, db_session):
    email = "failed.user@example.com"

    async def fake_send_message(*args, **kwargs):
        raise ConnectionError("SMTP auth failed")

    monkeypatch.setattr("app.controllers.signup_controller.FastMail.send_message", fake_send_message)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(request_signup_otp(SignupOTPRequest(email=email), db_session))

    assert exc_info.value.status_code == 503
    assert "Unable to send verification email" in exc_info.value.detail


def test_verify_signup_otp_creates_user(db_session):
    email = "verify.user@example.com"
    otp = "123456"
    hashed = bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()
    _pending_otps[email] = (hashed, datetime.now(timezone.utc) + timedelta(minutes=5))

    user = asyncio.run(verify_signup_otp(SignupOTPVerify(email=email, otp=otp), db_session))

    assert user.email == email
    assert user.email_verified is True
    assert email not in _pending_otps
