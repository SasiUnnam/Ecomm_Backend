# Search Engine API

This file documents the unified search API for the frontend.

## Endpoint

```http
GET /search?q={query}&limit={limit}
```

---

## Example request

```bash
curl "http://localhost:8000/search?q=iphone&limit=10"
```

---

## Example response

```json
{
  "query": "iphone",
  "total": 5,
  "products": [
    {
      "entity_type": "product",
      "id": 12,
      "name": "iPhone 17 Pro",
      "slug": "iphone-17-pro",
      "description": "Apple flagship smartphone",
      "brand": "Apple",
      "category_id": "CAT123e4567-e89b-12d3-a456-426614174000",
      "sub_category_id": "SUBCAT123e4567-e89b-12d3-a456-426614174001",
      "category_name": "Mobile Phones",
      "subcategory_name": "Apple iPhones",
      "score": 180.0,
      "match_fields": ["name", "brand", "category_name"]
    }
  ],
  "categories": [
    {
      "entity_type": "category",
      "id": "CAT123e4567-e89b-12d3-a456-426614174000",
      "name": "Mobile Phones",
      "slug": "mobile-phones",
      "score": 90.0,
      "match_fields": ["name"]
    }
  ],
  "subcategories": [
    {
      "entity_type": "subcategory",
      "id": "SUBCAT123e4567-e89b-12d3-a456-426614174001",
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
      "id": 12,
      "name": "iPhone 17 Pro",
      "score": 180.0
    }
  ]
}
```

---

## Frontend usage

```js
const query = 'iphone';
const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(query)}&limit=10`);
const result = await response.json();

console.log(result.products);
console.log(result.categories);
console.log(result.subcategories);
console.log(result.brands);
```

---

## Important notes

- `q` is required.
- `limit` is optional and defaults to `20`.
- `results` is the combined top-ranked list.
- `products` contains only product matches.
- `categories` contains category matches.
- `subcategories` contains subcategory matches.
- `brands` contains brand matches.

This is the main API for a unified product search experience in the frontend.
