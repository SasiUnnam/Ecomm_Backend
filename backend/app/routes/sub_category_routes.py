from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.sub_category_controller import (
    create_subcategory as create_subcategory_controller,
    delete_subcategory as delete_subcategory_controller,
    get_subcategories as get_subcategories_controller,
    get_subcategory as get_subcategory_controller,
    update_subcategory as update_subcategory_controller,
)
from app.schemas.sub_category import SubCategoryCreate, SubCategoryResponse, SubCategoryUpdate
from app.utils.identifiers import parse_subcategory_id

router = APIRouter(prefix="/subcategories", tags=["subcategories"])


@router.get("", response_model=list[SubCategoryResponse])
def get_subcategories(db: Session = Depends(get_db)) -> list[SubCategoryResponse]:
    return get_subcategories_controller(db)


@router.get("/{subcategory_id}", response_model=SubCategoryResponse)
def get_subcategory(subcategory_id: str, db: Session = Depends(get_db)) -> SubCategoryResponse:
    return get_subcategory_controller(parse_subcategory_id(subcategory_id), db)


@router.post("", response_model=SubCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    subcategory_data: SubCategoryCreate,
    db: Session = Depends(get_db),
) -> SubCategoryResponse:
    return create_subcategory_controller(subcategory_data, db)


@router.patch("/{subcategory_id}", response_model=SubCategoryResponse)
def update_subcategory(
    subcategory_id: str,
    subcategory_data: SubCategoryUpdate,
    db: Session = Depends(get_db),
) -> SubCategoryResponse:
    return update_subcategory_controller(parse_subcategory_id(subcategory_id), subcategory_data, db)


@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(subcategory_id: str, db: Session = Depends(get_db)) -> None:
    delete_subcategory_controller(parse_subcategory_id(subcategory_id), db)
    return None
