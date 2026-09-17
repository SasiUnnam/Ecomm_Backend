from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.sub_category import SubCategory
from app.schemas.sub_category import SubCategoryCreate, SubCategoryResponse, SubCategoryUpdate


def get_subcategories(db: Session) -> list[SubCategoryResponse]:
    return db.query(SubCategory).order_by(SubCategory.created_at.desc()).all()


def get_subcategory(subcategory_id: UUID, db: Session) -> SubCategoryResponse:
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory


def create_subcategory(subcategory_data: SubCategoryCreate, db: Session) -> SubCategoryResponse:
    slug = (subcategory_data.slug or "").strip().lower()
    if not slug:
        raise HTTPException(status_code=422, detail="Slug cannot be empty")

    category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_subcategory = db.query(SubCategory).filter(SubCategory.slug == slug).first()
    if existing_subcategory:
        raise HTTPException(status_code=400, detail="Subcategory with this slug already exists")

    subcategory = SubCategory(
        category_id=subcategory_data.category_id,
        name=subcategory_data.name,
        slug=slug,
        description=subcategory_data.description,
        image_url=subcategory_data.image_url,
        is_active=subcategory_data.is_active,
    )
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory


def update_subcategory(
    subcategory_id: UUID,
    subcategory_data: SubCategoryUpdate,
    db: Session,
) -> SubCategoryResponse:
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    updates = subcategory_data.model_dump(exclude_unset=True)

    if "category_id" in updates and updates["category_id"] is not None:
        category = db.query(Category).filter(Category.id == updates["category_id"]).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    if "slug" in updates and updates["slug"] is not None:
        slug = str(updates["slug"]).strip().lower()
        if not slug:
            raise HTTPException(status_code=422, detail="Slug cannot be empty")
        existing_subcategory = (
            db.query(SubCategory)
            .filter(SubCategory.slug == slug, SubCategory.id != subcategory_id)
            .first()
        )
        if existing_subcategory:
            raise HTTPException(status_code=400, detail="Subcategory with this slug already exists")
        subcategory.slug = slug
        updates.pop("slug")

    for field, value in updates.items():
        setattr(subcategory, field, value)

    db.commit()
    db.refresh(subcategory)
    return subcategory


def delete_subcategory(subcategory_id: UUID, db: Session) -> None:
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    db.delete(subcategory)
    db.commit()
