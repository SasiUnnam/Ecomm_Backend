# Category API Examples

This file shows example requests for the category endpoints.

## Base URL

```text
http://localhost:8000
```

---

## 1. Get all categories

### Request

```http
GET /categories
```

### Example

```bash
curl http://localhost:8000/categories
```

### Example response

```json
[
  {
    "id": "CAT1f2d3a7d-5a97-4d8c-bc3a-5e24dbd7f9a1",
    "name": "Electronics",
    "slug": "electronics",
    "description": "Devices and gadgets",
    "parent_id": null,
    "image_url": null,
    "is_active": true,
    "created_at": "2026-09-17T12:00:00Z",
    "updated_at": "2026-09-17T12:00:00Z"
  }
]
```

---

## 2. Get a single category

### Request

```http
GET /categories/{category_id}
```

### Example

```bash
curl http://localhost:8000/categories/CAT1f2d3a7d-5a97-4d8c-bc3a-5e24dbd7f9a1
```

---

## 3. Create a category

### Request

```http
POST /categories
Content-Type: application/json
```

### Example payload

```json
{
  "name": "Electronics",
  "slug": "electronics",
  "description": "Devices and gadgets",
  "parent_id": null,
  "image_url": "https://example.com/images/electronics.jpg",
  "is_active": true
}
```

### Example

```bash
curl -X POST http://localhost:8000/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "slug": "electronics",
    "description": "Devices and gadgets",
    "parent_id": null,
    "image_url": "https://example.com/images/electronics.jpg",
    "is_active": true
  }'
```

---

## 4. Update a category

### Request

```http
PATCH /categories/{category_id}
Content-Type: application/json
```

### Example payload

```json
{
  "name": "Home Appliances",
  "slug": "home-appliances",
  "description": "Kitchen and home products",
  "is_active": true
}
```

### Example

```bash
curl -X PATCH http://localhost:8000/categories/CAT1f2d3a7d-5a97-4d8c-bc3a-5e24dbd7f9a1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home Appliances",
    "slug": "home-appliances",
    "description": "Kitchen and home products",
    "is_active": true
  }'
```

---

## 5. Delete a category

### Request

```http
DELETE /categories/{category_id}
```

### Example

```bash
curl -X DELETE http://localhost:8000/categories/CAT1f2d3a7d-5a97-4d8c-bc3a-5e24dbd7f9a1
```

---

## Notes

- `id` values are returned in the format `CAT<uuid>`.
- `slug` must be unique.
- `parent_id` can be `null` for top-level categories.
- `is_active` determines whether the category is available for use.
- if you want a nested category, pass the parent category id in `parent_id`.

Example nested category payload:

```json
{
  "name": "Laptops",
  "slug": "laptops",
  "description": "Portable computers",
  "parent_id": "CAT11111111-2222-3333-4444-555555666666",
  "is_active": true
}
```
