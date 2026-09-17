from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.controllers.category_controller import create_category, delete_category, get_category, update_category
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def test_create_category_success(db_session):
    category = create_category(CategoryCreate(name="Phones", slug="phones", description="Smart phones"), db_session)

    assert category.slug == "phones"
    assert db_session.query(Category).filter_by(slug="phones").count() == 1


def test_update_category_rejects_duplicate_slug(db_session):
    create_category(CategoryCreate(name="Phones", slug="phones"), db_session)
    other = create_category(CategoryCreate(name="Laptops", slug="laptops"), db_session)

    with pytest.raises(HTTPException, match="already exists"):
        update_category(other.id, CategoryUpdate(slug="phones"), db_session)


def test_delete_category_removes_record(db_session):
    category = create_category(CategoryCreate(name="Accessories", slug="accessories"), db_session)

    delete_category(category.id, db_session)

    assert db_session.query(Category).filter_by(id=category.id).count() == 0
    with pytest.raises(HTTPException):
        get_category(category.id, db_session)
