import pytest
from fastapi import HTTPException

from app.controllers.category_controller import create_category
from app.controllers.product_controller import create_product
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.schemas.category import CategoryCreate
from app.schemas.product import ProductCreate


def test_create_product_success(db_session):
    category = create_category(CategoryCreate(name="Electronics", slug="electronics"), db_session)
    subcategory = SubCategory(
        category_id=category.id,
        name="Smartphones",
        slug="smartphones",
        description="Mobile phones",
        is_active=True,
    )
    db_session.add(subcategory)
    db_session.commit()
    db_session.refresh(subcategory)

    product = create_product(
        ProductCreate(
            category_id=category.id,
            sub_category_id=subcategory.id,
            sku="SKU-1",
            name="iPhone 15",
            slug="iphone-15",
            description="Latest iPhone",
            price="999.99",
            compare_at_price="1099.99",
            brand="Apple",
            specifications={"color": "blue"},
            status="active",
            is_featured=True,
        ),
        db_session,
    )

    assert product.name == "iPhone 15"
    assert db_session.query(Product).filter_by(sku="SKU-1").count() == 1


def test_create_product_rejects_duplicate_slug(db_session):
    category = create_category(CategoryCreate(name="Electronics", slug="electronics"), db_session)
    subcategory = SubCategory(
        category_id=category.id,
        name="Smartphones",
        slug="smartphones",
        description="Mobile phones",
        is_active=True,
    )
    db_session.add(subcategory)
    db_session.commit()
    db_session.refresh(subcategory)

    create_product(
        ProductCreate(
            category_id=category.id,
            sub_category_id=subcategory.id,
            sku="SKU-2",
            name="iPhone 15",
            slug="iphone-15",
            description="Latest iPhone",
            price="999.99",
            compare_at_price="1099.99",
            brand="Apple",
            specifications={"color": "blue"},
            status="active",
            is_featured=True,
        ),
        db_session,
    )

    with pytest.raises(HTTPException, match="already exists"):
        create_product(
            ProductCreate(
                category_id=category.id,
                sub_category_id=subcategory.id,
                sku="SKU-3",
                name="Duplicate iPhone",
                slug="iphone-15",
                description="Duplicate",
                price="899.99",
                brand="Apple",
                status="active",
                is_featured=False,
            ),
            db_session,
        )
