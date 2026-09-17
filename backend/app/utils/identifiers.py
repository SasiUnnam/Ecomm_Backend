from uuid import UUID

from fastapi import HTTPException


USER_ID_PREFIX = "TN"
CATEGORY_ID_PREFIX = "CAT"
SUBCATEGORY_ID_PREFIX = "SUBCAT"


def format_user_id(user_id: UUID) -> str:
    return f"{USER_ID_PREFIX}{user_id}"


def parse_user_id(value: str) -> UUID:
    normalized_value = value.removeprefix(USER_ID_PREFIX)
    try:
        return UUID(normalized_value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid user ID") from exc


def format_category_id(category_id: UUID) -> str:
    return f"{CATEGORY_ID_PREFIX}{category_id}"


def parse_category_id(value: str) -> UUID:
    normalized_value = value.removeprefix(CATEGORY_ID_PREFIX)
    try:
        return UUID(normalized_value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid category ID") from exc


def format_subcategory_id(subcategory_id: UUID) -> str:
    return f"{SUBCATEGORY_ID_PREFIX}{subcategory_id}"


def parse_subcategory_id(value: str) -> UUID:
    normalized_value = value.removeprefix(SUBCATEGORY_ID_PREFIX)
    try:
        return UUID(normalized_value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid subcategory ID") from exc