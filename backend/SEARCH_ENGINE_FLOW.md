# Search Engine Flow

This document explains how the unified search feature works in the backend and how the frontend can use it.

---

## 1. Goal

The search engine is designed to return relevant results across the catalog for a single user query.

Example:

```text
Query: iphone
```

The API should match:

- product names
- product descriptions
- product brand names
- category names
- subcategory names
- product specifications values
- related catalog hierarchy

It should not return unrelated products just because they belong to a matching category.

---

## 2. Search behavior

The search engine works in this order:

1. Normalize the query
   - lowercase
   - remove extra spaces
   - remove punctuation
   - split into searchable tokens

2. Search all major catalog entities
   - products
   - categories
   - subcategories
   - brands

3. Score every result based on relevance
   - exact matches get higher weight
   - partial matches get a medium score
   - token matches get a smaller score
   - related category/subcategory names boost the product score
   - JSONB specifications can also contribute to relevance

4. Sort results by score descending

5. Return a combined ranked result list

---

## 3. Relevance example

For the search:

```text
iphone
```

A product such as:

```text
iPhone 17 Pro
```

will rank highly because:

- the name contains `iphone`
- the slug may contain `iphone`
- the brand may be `Apple`
- the category or subcategory may be related to mobile phones
- the product description may mention iPhone features
- JSONB specification data may include terms like `ios`, `camera`, `5g`

A product with only a category match will rank lower unless its actual product text also matches.

---

## 4. Search flow in the app

### Backend flow

```text
Frontend request
    -> GET /search?q=iphone
    -> search_routes.py
    -> unified_search(...) in search_controller.py
    -> read products, categories, subcategories
    -> compute relevance score for each record
    -> sort by score descending
    -> return SearchResponse
```

### Main logic in the controller

The controller:

- accepts a query string
- validates it is not empty
- tokenizes it into searchable words
- checks product fields such as:
  - name
  - slug
  - description
  - brand
  - specifications
- checks category and subcategory names
- calculates relevance score
- merges results across entity types

---

## 5. Current search fields

### Products are searched in:

- `name`
- `slug`
- `description`
- `brand`
- `category.name`
- `sub_category.name`
- `specifications` JSONB

### Categories are searched in:

- `name`
- `slug`
- `description`

### Subcategories are searched in:

- `name`
- `slug`
- `description`
- parent category name

### Brands are searched in:

- `product.brand`

---

## 6. API endpoint

### Request

```http
GET /search?q=iphone&limit=20
```

### Query params

- `q` — required search term
- `limit` — optional maximum number of results to return

### Example

```bash
curl "http://localhost:8000/search?q=iphone&limit=20"
```

---

## 7. Response format

```json
{
  "query": "iphone",
  "total": 12,
  "products": [
    {
      "entity_type": "product",
      "id": 14,
      "name": "iPhone 17 Pro",
      "slug": "iphone-17-pro",
      "description": "Apple flagship smartphone",
      "brand": "Apple",
      "category_id": "CAT...",
      "sub_category_id": "SUBCAT...",
      "category_name": "Mobile Phones",
      "subcategory_name": "Apple iPhones",
      "score": 190.0,
      "match_fields": ["name", "brand", "category_name"]
    }
  ],
  "categories": [
    {
      "entity_type": "category",
      "id": "CAT...",
      "name": "Mobile Phones",
      "slug": "mobile-phones",
      "score": 90.0,
      "match_fields": ["name"]
    }
  ],
  "subcategories": [
    {
      "entity_type": "subcategory",
      "id": "SUBCAT...",
      "name": "Apple iPhones",
      "slug": "apple-iphones",
      "score": 110.0,
      "match_fields": ["name"]
    }
  ],
  "brands": [
    {
      "entity_type": "brand",
      "id": "Apple",
      "name": "Apple",
      "score": 80.0,
      "match_fields": ["brand"]
    }
  ],
  "results": [
    {
      "entity_type": "product",
      "id": 14,
      "name": "iPhone 17 Pro",
      "score": 190.0
    }
  ]
}
```

---

## 8. Why this is powerful

This search is stronger than a basic category filter because it understands:

- keyword matching across real product data
- product metadata and JSONB specs
- category and subcategory relationships
- product brand relevance
- score-based ranking instead of simple inclusion

This helps users search naturally, even when they type broad or partial product names.

---

## 9. Example frontend usage

```js
const query = 'iphone';

const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(query)}&limit=20`);
const data = await response.json();

console.log(data.products);
console.log(data.categories);
console.log(data.subcategories);
console.log(data.brands);
```

Front-end can then:

- show product cards from `data.products`
- show category suggestions from `data.categories`
- show subcategory suggestions from `data.subcategories`
- show brand chips from `data.brands`

---

## 10. Best practice

For a large catalog, later you can improve this with:

- PostgreSQL full-text search (`tsvector`)
- trigram similarity (`pg_trgm`)
- search indexing for product names and specs
- rank tuning for exact vs fuzzy matches
- filter by category, brand, price, or stock

But the current version already gives a strong unified search experience for a normal e-commerce backend.
