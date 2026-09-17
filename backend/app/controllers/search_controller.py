import re
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.schemas.search import SearchItem, SearchResponse


def _normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def _tokenize(query: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", _normalize_text(query)) if len(token) >= 2]


def _field_score(field_value: str | None, tokens: list[str], full_query: str) -> tuple[float, list[str]]:
    text = _normalize_text(field_value)
    if not text:
        return 0.0, []

    score = 0.0
    match_fields: list[str] = []
    full_query_norm = _normalize_text(full_query)

    if full_query_norm and full_query_norm == text:
        score += 120
        match_fields.append("exact")
    elif full_query_norm and full_query_norm in text:
        score += 70
        match_fields.append("contains")

    for token in tokens:
        if token in text:
            score += 25
            match_fields.append(token)
            if text.startswith(token):
                score += 30

    if full_query_norm and len(tokens) > 1:
        token_matches = sum(1 for token in tokens if token in text)
        if token_matches == len(tokens):
            score += 40

    return score, list(dict.fromkeys(match_fields))


def _build_category_result(category: Category, tokens: list[str], full_query: str) -> SearchItem:
    score, match_fields = _field_score(category.name, tokens, full_query)
    score += _field_score(category.slug, tokens, full_query)[0] * 1.2
    score += _field_score(category.description, tokens, full_query)[0] * 0.8

    result = SearchItem(
        entity_type="category",
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        description=category.description,
        score=round(score, 2),
        match_fields=match_fields,
    )
    if not result.match_fields:
        result.match_fields = ["name"] if category.name else []
    return result


def _build_subcategory_result(subcategory: SubCategory, tokens: list[str], full_query: str) -> SearchItem:
    score, match_fields = _field_score(subcategory.name, tokens, full_query)
    score += _field_score(subcategory.slug, tokens, full_query)[0] * 1.2
    score += _field_score(subcategory.description, tokens, full_query)[0] * 0.8

    category_name = subcategory.category.name if subcategory.category else None
    score += _field_score(category_name, tokens, full_query)[0] * 0.5

    result = SearchItem(
        entity_type="subcategory",
        id=str(subcategory.id),
        name=subcategory.name,
        slug=subcategory.slug,
        description=subcategory.description,
        category_id=str(subcategory.category_id),
        category_name=category_name,
        score=round(score, 2),
        match_fields=match_fields,
    )
    if not result.match_fields:
        result.match_fields = ["name"] if subcategory.name else []
    return result


def _build_product_result(product: Product, tokens: list[str], full_query: str) -> SearchItem:
    score = 0.0
    match_fields: list[str] = []

    for field_name, field_value in [
        ("name", product.name),
        ("slug", product.slug),
        ("description", product.description),
        ("brand", product.brand),
    ]:
        value_score, value_matches = _field_score(field_value, tokens, full_query)
        score += value_score
        match_fields.extend(value_matches)
        if field_name == "name":
            score += 20

    if product.category:
        category_score, category_matches = _field_score(product.category.name, tokens, full_query)
        score += category_score * 0.8
        match_fields.extend(category_matches)

    if product.sub_category:
        subcategory_score, subcategory_matches = _field_score(product.sub_category.name, tokens, full_query)
        score += subcategory_score * 0.8
        match_fields.extend(subcategory_matches)

    if product.specifications:
        specs_text = str(product.specifications).lower()
        spec_score = 0.0
        for token in tokens:
            if token in specs_text:
                spec_score += 18
        score += spec_score
        if spec_score > 0:
            match_fields.append("specifications")

    result = SearchItem(
        entity_type="product",
        id=product.id,
        name=product.name,
        slug=product.slug,
        description=product.description,
        brand=product.brand,
        category_id=str(product.category_id),
        sub_category_id=str(product.sub_category_id),
        category_name=product.category.name if product.category else None,
        subcategory_name=product.sub_category.name if product.sub_category else None,
        score=round(score, 2),
        match_fields=list(dict.fromkeys(match_fields)),
    )
    if not result.match_fields:
        result.match_fields = ["name"] if product.name else []
    return result


def _build_brand_result(product: Product, tokens: list[str], full_query: str) -> SearchItem | None:
    brand_name = (product.brand or "").strip()
    if not brand_name:
        return None

    text = _normalize_text(brand_name)
    if not text:
        return None
    if full_query and full_query.lower() not in text and not any(token in text for token in tokens):
        return None

    score, match_fields = _field_score(brand_name, tokens, full_query)
    return SearchItem(
        entity_type="brand",
        id=brand_name,
        name=brand_name,
        description=f"Brand matched in product catalog",
        brand=brand_name,
        score=round(score + 25, 2),
        match_fields=match_fields or ["brand"],
    )


def unified_search(db: Session, query: str, limit: int = 20) -> SearchResponse:
    trimmed_query = (query or "").strip()
    if not trimmed_query:
        raise HTTPException(status_code=400, detail="Search query is required")

    tokens = _tokenize(trimmed_query)
    if not tokens:
        raise HTTPException(status_code=400, detail="Please enter a valid search term")

    categories = db.query(Category).all()
    subcategories = db.query(SubCategory).all()
    products = db.query(Product).all()

    category_items = [
        _build_category_result(category, tokens, trimmed_query)
        for category in categories
    ]
    category_items = [item for item in category_items if item.score > 0]
    category_items.sort(key=lambda item: item.score, reverse=True)

    subcategory_items = [
        _build_subcategory_result(subcategory, tokens, trimmed_query)
        for subcategory in subcategories
    ]
    subcategory_items = [item for item in subcategory_items if item.score > 0]
    subcategory_items.sort(key=lambda item: item.score, reverse=True)

    product_items = [
        _build_product_result(product, tokens, trimmed_query)
        for product in products
    ]
    product_items = [item for item in product_items if item.score > 0]
    product_items.sort(key=lambda item: item.score, reverse=True)

    brand_map: dict[str, SearchItem] = {}
    for product in products:
        brand_item = _build_brand_result(product, tokens, trimmed_query)
        if brand_item:
            brand_map.setdefault(brand_item.name, brand_item)
            brand_map[brand_item.name].score = max(brand_map[brand_item.name].score, brand_item.score)
            brand_map[brand_item.name].match_fields = list(
                dict.fromkeys(brand_map[brand_item.name].match_fields + brand_item.match_fields)
            )

    brand_items = sorted(brand_map.values(), key=lambda item: item.score, reverse=True)

    all_results = product_items + category_items + subcategory_items + brand_items
    all_results.sort(key=lambda item: item.score, reverse=True)
    all_results = all_results[:limit]

    response = SearchResponse(
        query=trimmed_query,
        total=len(all_results),
        products=product_items[:limit],
        categories=category_items[:limit],
        subcategories=subcategory_items[:limit],
        brands=brand_items[:limit],
        results=all_results,
    )
    return response
