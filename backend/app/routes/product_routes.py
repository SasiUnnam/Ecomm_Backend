from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.product_controller import (
    create_product as create_product_controller,
    delete_product as delete_product_controller,
    get_product as get_product_controller,
    get_products as get_products_controller,
    update_product as update_product_controller,
)
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    return get_products_controller(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    return get_product_controller(product_id, db)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductResponse:
    return create_product_controller(product_data, db)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
) -> ProductResponse:
    return update_product_controller(product_id, product_data, db)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    delete_product_controller(product_id, db)
    return None
