# Product Frontend API

This file is only for product-related frontend API usage.

## Base URL

```text
http://localhost:8000
```

---

## 1. Get all products

```http
GET /products
```

Example:

```bash
curl http://localhost:8000/products
```

Use this to show all products on the homepage, catalog page, or product list page.

### Example response

```json
[
  {
    "id": 1,
    "category_id": "CAT123e4567-e89b-12d3-a456-426614174000",
    "sub_category_id": "SUBCAT123e4567-e89b-12d3-a456-426614174001",
    "sku": "LAP-001",
    "name": "Dell XPS 13",
    "slug": "dell-xps-13",
    "description": "Thin and light premium laptop",
    "price": 1299.99,
    "compare_at_price": 1499.99,
    "brand": "Dell",
    "specifications": {
      "ram": "16GB",
      "storage": "512GB SSD",
      "color": "Silver"
    },
    "status": "active",
    "is_featured": true,
    "created_at": "2026-09-17T12:00:00Z",
    "updated_at": "2026-09-17T12:00:00Z"
  }
]
```

---

## 2. Get one product

```http
GET /products/{product_id}
```

Example:

```bash
curl http://localhost:8000/products/1
```

Use this for the product detail page.

---

## 3. Create product

```http
POST /products
```

Example request body:

```json
{
  "category_id": "CAT123e4567-e89b-12d3-a456-426614174000",
  "sub_category_id": "SUBCAT123e4567-e89b-12d3-a456-426614174001",
  "sku": "LAP-001",
  "name": "Dell XPS 13",
  "slug": "dell-xps-13",
  "description": "Thin and light premium laptop",
  "price": 1299.99,
  "compare_at_price": 1499.99,
  "brand": "Dell",
  "specifications": {
    "ram": "16GB",
    "storage": "512GB SSD",
    "color": "Silver"
  },
  "status": "active",
  "is_featured": true
}
```

Example:

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "category_id": "CAT123e4567-e89b-12d3-a456-426614174000",
    "sub_category_id": "SUBCAT123e4567-e89b-12d3-a456-426614174001",
    "sku": "LAP-001",
    "name": "Dell XPS 13",
    "slug": "dell-xps-13",
    "description": "Thin and light premium laptop",
    "price": 1299.99,
    "compare_at_price": 1499.99,
    "brand": "Dell",
    "specifications": {"ram": "16GB", "storage": "512GB SSD", "color": "Silver"},
    "status": "active",
    "is_featured": true
  }'
```

---

## 4. Update product

```http
PATCH /products/{product_id}
```

Example request body:

```json
{
  "name": "Dell XPS 14",
  "price": 1399.99,
  "is_featured": false,
  "status": "active"
}
```

Example:

```bash
curl -X PATCH http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dell XPS 14",
    "price": 1399.99,
    "is_featured": false,
    "status": "active"
  }'
```

---

## 5. Delete product

```http
DELETE /products/{product_id}
```

Example:

```bash
curl -X DELETE http://localhost:8000/products/1
```

---

## Frontend usage

### Fetch all products

```js
const response = await fetch('http://localhost:8000/products');
const products = await response.json();
console.log(products);
```

### Fetch one product by id

```js
const productId = 1;
const response = await fetch(`http://localhost:8000/products/${productId}`);
const product = await response.json();
console.log(product);
```

### Filter products by category

```js
const products = await fetch('http://localhost:8000/products').then(r => r.json());
const selectedCategoryId = 'CAT123e4567-e89b-12d3-a456-426614174000';

const categoryProducts = products.filter(
  product => product.category_id === selectedCategoryId
);
```

### Filter products by subcategory

```js
const selectedSubCategoryId = 'SUBCAT123e4567-e89b-12d3-a456-426614174001';

const subCategoryProducts = products.filter(
  product => product.sub_category_id === selectedSubCategoryId
);
```

---

## Important notes

- `category_id` is required for every product.
- `sub_category_id` is required for every product.
- `sku` must be unique.
- `slug` must be unique.
- `price` should be sent as a number, not a string.
- `compare_at_price` is optional.
- `specifications` is a JSON object and can be used for product details.

This is the main product API your frontend should use for product listing, product detail, and product management.
