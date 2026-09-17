def sample_user_payload(email: str = "demo@example.com") -> dict:
    return {
        "first_name": "Demo",
        "last_name": "User",
        "email": email,
        "password": "StrongPass123!",
        "role": "user",
        "phone": "+1234567890",
        "profile_pic_url": "https://example.com/avatar.png",
        "is_active": True,
        "email_verified": False,
    }
