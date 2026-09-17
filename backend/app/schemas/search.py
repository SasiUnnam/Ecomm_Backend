from typing import Any

from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    entity_type: str
    id: str | int
    name: str
    slug: str | None = None
    description: str | None = None
    brand: str | None = None
    category_id: str | None = None
    sub_category_id: str | None = None
    category_name: str | None = None
    subcategory_name: str | None = None
    score: float = 0.0
    match_fields: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    query: str
    total: int
    products: list[SearchItem] = Field(default_factory=list)
    categories: list[SearchItem] = Field(default_factory=list)
    subcategories: list[SearchItem] = Field(default_factory=list)
    brands: list[SearchItem] = Field(default_factory=list)
    results: list[SearchItem] = Field(default_factory=list)
