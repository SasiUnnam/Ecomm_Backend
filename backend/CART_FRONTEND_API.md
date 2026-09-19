# Cart Frontend API Documentation

This document provides complete instructions, endpoint specifications, payload examples, and frontend integration code for the Shopping Cart API.

## Base URL

```text
http://localhost:8000
```

---

## Overview & User ID Formatting

- All cart operations associate a cart with a specific user.
- User IDs can be supplied as raw UUIDs (`123e4567-e89b-12d3-a456-426614174000`) or prefixed with `TN` (`TN123e4567-e89b-12d3-a456-426614174000`).
- Responses serialize `user_id` with the `TN` prefix for frontend consistency.
- When an item is added that is already in the cart, the quantity is automatically incremented.

---

## Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/carts` | List all carts (paginated) |
| `POST` | `/carts` | Create a new cart for a user |
| `GET` | `/carts/user/{user_id}` | Get active cart by User ID |
| `GET` | `/carts/{cart_id}` | Get cart by Cart ID |
| `PATCH` | `/carts/{cart_id}` | Update cart status |
| `DELETE` | `/carts/{cart_id}` | Delete a cart |
| `POST` | `/carts/{cart_id}/clear` | Remove all items from cart |
| `GET` | `/carts/{cart_id}/items` | List items inside a cart |
| `POST` | `/carts/{cart_id}/items` | Add a product to a cart |
| `GET` | `/carts/{cart_id}/items/{item_id}` | Get a single cart item |
| `PATCH` | `/carts/{cart_id}/items/{item_id}` | Update cart item quantity/price |
| `DELETE` | `/carts/{cart_id}/items/{item_id}` | Remove an item from cart |

---

## 1. Get or Create Cart for User

### Check if User has a Cart

```http
GET /carts/user/{user_id}
```

**Example:**
```bash
curl http://localhost:8000/carts/user/TN123e4567-e89b-12d3-a456-426614174000
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "status": "active",
  "created_at": "2026-09-19T10:00:00Z",
  "updated_at": "2026-09-19T10:00:00Z",
  "items": [
    {
      "id": 10,
      "cart_id": 1,
      "product_id": 4,
      "quantity": 2,
      "unit_price": "49.99",
      "created_at": "2026-09-19T10:05:00Z",
      "updated_at": "2026-09-19T10:05:00Z"
    }
  ]
}
```

### Create Cart (if not exists)

```http
POST /carts
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "status": "active"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/carts \
  -H "Content-Type: application/json" \
  -d '{"user_id": "TN123e4567-e89b-12d3-a456-426614174000", "status": "active"}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "status": "active",
  "created_at": "2026-09-19T10:00:00Z",
  "updated_at": "2026-09-19T10:00:00Z",
  "items": []
}
```

---

## 2. Add Item to Cart

```http
POST /carts/{cart_id}/items
Content-Type: application/json
```

> **Note:** `unit_price` is optional. If omitted, the server automatically uses the current `price` from the `Product` table.

**Request Body:**
```json
{
  "product_id": 4,
  "quantity": 1,
  "unit_price": "49.99"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/carts/1/items \
  -H "Content-Type: application/json" \
  -d '{"product_id": 4, "quantity": 1}'
```

**Response (201 Created):**
```json
{
  "id": 10,
  "cart_id": 1,
  "product_id": 4,
  "quantity": 1,
  "unit_price": "49.99",
  "created_at": "2026-09-19T10:05:00Z",
  "updated_at": "2026-09-19T10:05:00Z"
}
```

---

## 3. Update Cart Item (Quantity)

```http
PATCH /carts/{cart_id}/items/{item_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "quantity": 3
}
```

**Example:**
```bash
curl -X PATCH http://localhost:8000/carts/1/items/10 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3}'
```

**Response (200 OK):**
```json
{
  "id": 10,
  "cart_id": 1,
  "product_id": 4,
  "quantity": 3,
  "unit_price": "49.99",
  "created_at": "2026-09-19T10:05:00Z",
  "updated_at": "2026-09-19T10:07:00Z"
}
```

---

## 4. Remove Item from Cart

```http
DELETE /carts/{cart_id}/items/{item_id}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/carts/1/items/10
```

**Response:** `204 No Content`

---

## 5. Clear All Items in Cart

```http
POST /carts/{cart_id}/clear
```

**Example:**
```bash
curl -X POST http://localhost:8000/carts/1/clear
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "status": "active",
  "created_at": "2026-09-19T10:00:00Z",
  "updated_at": "2026-09-19T10:08:00Z",
  "items": []
}
```

---

## 6. Update Cart Status

```http
PATCH /carts/{cart_id}
Content-Type: application/json
```

Status can be `"active"`, `"converted"`, or `"abandoned"`.

**Request Body:**
```json
{
  "status": "converted"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "status": "converted",
  "created_at": "2026-09-19T10:00:00Z",
  "updated_at": "2026-09-19T10:10:00Z",
  "items": []
}
```

---

## Frontend Integration Examples (JavaScript / TypeScript)

### Helper: Get or Initialize User Cart

```javascript
const API_BASE = 'http://localhost:8000';

export async function getOrCreateCart(userId) {
  // 1. Try to fetch existing cart
  let res = await fetch(`${API_BASE}/carts/user/${userId}`);
  if (res.status === 200) {
    return await res.json();
  }

  // 2. If 404, create a new cart
  if (res.status === 404) {
    const createRes = await fetch(`${API_BASE}/carts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, status: 'active' }),
    });
    return await createRes.json();
  }

  throw new Error('Failed to load user cart');
}
```

### Add to Cart on Product Page

```javascript
export async function handleAddToCart(cartId, productId, quantity = 1) {
  const response = await fetch(`${API_BASE}/carts/${cartId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity
    }),
  });

  if (!response.ok) {
    throw new Error('Could not add product to cart');
  }

  return await response.json();
}
```

### Update Item Quantity in Cart View

```javascript
export async function updateItemQuantity(cartId, itemId, newQuantity) {
  if (newQuantity <= 0) {
    // Remove if quantity reaches zero
    await fetch(`${API_BASE}/carts/${cartId}/items/${itemId}`, { method: 'DELETE' });
    return null;
  }

  const response = await fetch(`${API_BASE}/carts/${cartId}/items/${itemId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quantity: newQuantity }),
  });

  return await response.json();
}
```
