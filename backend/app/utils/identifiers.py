from uuid import UUID

from fastapi import HTTPException


USER_ID_PREFIX = "TN"


def format_user_id(user_id: UUID) -> str:
    return f"{USER_ID_PREFIX}{user_id}"


def parse_user_id(value: str) -> UUID:
    normalized_value = value.removeprefix(USER_ID_PREFIX)
    try:
        return UUID(normalized_value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid user ID") from exc