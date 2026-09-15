import secrets
import string


def generate_otp(length: int = 6) -> str:
    """Generate a cryptographically secure numeric one-time password."""
    if length < 4 or length > 10:
        raise ValueError("OTP length must be between 4 and 10 digits")

    return "".join(secrets.choice(string.digits) for _ in range(length))
