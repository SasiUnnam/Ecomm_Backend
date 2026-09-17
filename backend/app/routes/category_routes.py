from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.category_controller import (
    create_category as create_category_controller,
    delete_category as delete_category_controller,
    get_categories as get_categories_controller,
    get_category as get_category_controller,
    update_category as update_category_controller,
)
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.utils.identifiers import parse_category_id

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)) -> list[CategoryResponse]:
    return get_categories_controller(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, db: Session = Depends(get_db)) -> CategoryResponse:
    return get_category_controller(parse_category_id(category_id), db)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    return create_category_controller(category_data, db)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    return update_category_controller(parse_category_id(category_id), category_data, db)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    delete_category_controller(parse_category_id(category_id), db)
    return None
