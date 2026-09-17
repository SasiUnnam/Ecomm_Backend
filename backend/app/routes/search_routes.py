from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.controllers.search_controller import unified_search
from app.schemas.search import SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search_catalog(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> SearchResponse:
    return unified_search(db, q, limit=limit)
