from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate


def get_products(db: Session) -> list[ProductResponse]:
    return db.query(Product).order_by(Product.created_at.desc()).all()


def get_product(product_id: int, db: Session) -> ProductResponse:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create_product(product_data: ProductCreate, db: Session) -> ProductResponse:
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    subcategory = (
        db.query(SubCategory)
        .filter(SubCategory.id == product_data.sub_category_id)
        .first()
    )
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    if subcategory.category_id != product_data.category_id:
        raise HTTPException(
            status_code=400,
            detail="Subcategory does not belong to the selected category",
        )

    existing_by_sku = db.query(Product).filter(Product.sku == product_data.sku).first()
    if existing_by_sku:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")

    existing_by_slug = db.query(Product).filter(Product.slug == product_data.slug).first()
    if existing_by_slug:
        raise HTTPException(status_code=400, detail="Product with this slug already exists")

    product = Product(
        category_id=product_data.category_id,
        sub_category_id=product_data.sub_category_id,
        sku=product_data.sku,
        name=product_data.name,
        slug=product_data.slug,
        description=product_data.description,
        price=product_data.price,
        compare_at_price=product_data.compare_at_price,
        brand=product_data.brand,
        specifications=product_data.specifications,
        status=product_data.status,
        is_featured=product_data.is_featured,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(product_id: int, product_data: ProductUpdate, db: Session) -> ProductResponse:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = product_data.model_dump(exclude_unset=True)

    if "category_id" in updates and updates["category_id"] is not None:
        category = db.query(Category).filter(Category.id == updates["category_id"]).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    if "sub_category_id" in updates and updates["sub_category_id"] is not None:
        subcategory = (
            db.query(SubCategory)
            .filter(SubCategory.id == updates["sub_category_id"])
            .first()
        )
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")

        selected_category_id = updates.get("category_id", product.category_id)
        if subcategory.category_id != selected_category_id:
            raise HTTPException(
                status_code=400,
                detail="Subcategory does not belong to the selected category",
            )

    if "sku" in updates and updates["sku"] is not None:
        existing_by_sku = (
            db.query(Product)
            .filter(Product.sku == updates["sku"], Product.id != product_id)
            .first()
        )
        if existing_by_sku:
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")

    if "slug" in updates and updates["slug"] is not None:
        existing_by_slug = (
            db.query(Product)
            .filter(Product.slug == updates["slug"], Product.id != product_id)
            .first()
        )
        if existing_by_slug:
            raise HTTPException(status_code=400, detail="Product with this slug already exists")

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(product_id: int, db: Session) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
