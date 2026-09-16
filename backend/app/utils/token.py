import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone

from app.configs.settings import settings


def generate_token(nbytes: int = 32) -> str:
    """Generate a cryptographically secure URL-safe token."""
    if nbytes < 16:
        raise ValueError("Token size must be at least 16 bytes")

    return secrets.token_urlsafe(nbytes)


def _encode_part(value: dict[str, object]) -> str:
    encoded = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return base64.urlsafe_b64encode(encoded).rstrip(b"=").decode()


def create_token(subject: str | int, token_type: str, expires_delta: timedelta) -> str:
    """Create a signed JWT for the given subject and token type."""
    if settings.algorithm != "HS256":
        raise ValueError("Only the HS256 signing algorithm is supported")

    now = datetime.now(timezone.utc)
    header = {"alg": settings.algorithm, "typ": "JWT"}
    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "jti": generate_token(16),
    }
    signing_input = f"{_encode_part(header)}.{_encode_part(payload)}"
    signature = hmac.new(
        settings.secret_key.encode(), signing_input.encode(), hashlib.sha256
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    return f"{signing_input}.{encoded_signature}"


def create_access_token(subject: str | int) -> str:
    """Create a short-lived access token."""
    return create_token(
        subject,
        "access",
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(subject: str | int) -> str:
    """Create a long-lived refresh token."""
    return create_token(
        subject,
        "refresh",
        timedelta(days=settings.refresh_token_expire_days),
    )
