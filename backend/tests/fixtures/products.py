from uuid import uuid4


def sample_product_payload(category_id, sub_category_id):
    return {
        "category_id": category_id,
        "sub_category_id": sub_category_id,
        "sku": "SKU-IPHONE-001",
        "name": "iPhone 15 Pro",
        "slug": "iphone-15-pro",
        "description": "A premium smartphone with smart camera features.",
        "price": "999.99",
        "compare_at_price": "1199.99",
        "brand": "Apple",
        "specifications": {"color": "black titanium", "storage": "256GB"},
        "status": "active",
        "is_featured": True,
    }
