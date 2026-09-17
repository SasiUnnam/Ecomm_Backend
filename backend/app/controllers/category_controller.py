from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


def get_categories(db: Session) -> list[CategoryResponse]:
    return db.query(Category).order_by(Category.created_at.desc()).all()


def get_category(category_id: UUID, db: Session) -> CategoryResponse:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(category_data: CategoryCreate, db: Session) -> CategoryResponse:
    slug = (category_data.slug or "").strip().lower()
    if not slug:
        raise HTTPException(status_code=422, detail="Slug cannot be empty")

    existing_category = db.query(Category).filter(Category.slug == slug).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")

    category = Category(
        name=category_data.name,
        slug=slug,
        description=category_data.description,
        image_url=category_data.image_url,
        is_active=category_data.is_active,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session,
) -> CategoryResponse:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    updates = category_data.model_dump(exclude_unset=True)

    if "slug" in updates and updates["slug"] is not None:
        slug = str(updates["slug"]).strip().lower()
        if not slug:
            raise HTTPException(status_code=422, detail="Slug cannot be empty")
        existing_category = (
            db.query(Category)
            .filter(Category.slug == slug, Category.id != category_id)
            .first()
        )
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this slug already exists")
        category.slug = slug
        updates.pop("slug")

    for field, value in updates.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(category_id: UUID, db: Session) -> None:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
