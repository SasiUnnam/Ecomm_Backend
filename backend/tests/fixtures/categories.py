from uuid import uuid4


def sample_category_payload(name: str = "Electronics", slug: str = "electronics") -> dict:
    return {
        "name": name,
        "slug": slug,
        "description": "Popular electronic devices",
        "image_url": "https://example.com/categories/electronics.jpg",
        "is_active": True,
    }


def sample_category_model(name: str = "Electronics", slug: str = "electronics"):
    return {
        "id": uuid4(),
        "name": name,
        "slug": slug,
        "description": "Popular electronic devices",
        "image_url": "https://example.com/categories/electronics.jpg",
        "is_active": True,
    }
