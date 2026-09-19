# Order Frontend API Documentation

This document provides complete instructions, endpoint specifications, payload examples, and frontend integration code for the Orders & Order Items API.

## Base URL

```text
http://localhost:8000
```

---

## Key Features & Business Rules

1. **User ID Support**:
   - `user_id` can be sent as a standard UUID (`123e4567-e89b-12d3-a456-426614174000`) or prefixed with `TN` (`TN123e4567-e89b-12d3-a456-426614174000`).
   - Responses always serialize `user_id` formatted with the `TN` prefix for frontend consistency.
2. **Order Number Generation**:
   - If `order_number` is not provided during creation, the server automatically generates a unique human-friendly order identifier (e.g. `ORD-20260919143000-A1B2C3`).
3. **Product Snapshot**:
   - Order items automatically take a immutable snapshot of `product_name`, `sku`, and `unit_price` at the moment of order placement.
4. **Automatic Calculations**:
   - `subtotal` = Sum of all item line totals (`quantity * unit_price`).
   - `total_amount` = `subtotal - discount_amount + tax_amount + shipping_amount`.
5. **Direct Cart Checkout**:
   - `POST /orders/from-cart/{user_id}` automatically transfers active cart items into an order and transitions the cart status to `"converted"`.
6. **Automatic Timestamps**:
   - Updating status to `"placed"` automatically sets `placed_at` to the current UTC timestamp if not previously set.

---

## Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/orders` | List orders (supports filters: `status`, `payment_status`, `user_id`) |
| `POST` | `/orders` | Create an order directly (with optional items) |
| `POST` | `/orders/from-cart/{user_id}` | Convert an active user cart into an order (Checkout) |
| `GET` | `/orders/{order_id}` | Get order details by internal ID |
| `GET` | `/orders/number/{order_number}` | Get order details by customer-facing order number |
| `GET` | `/orders/user/{user_id}` | List all orders for a specific user (Order History) |
| `PATCH` | `/orders/{order_id}` | Update order (status, payment status, addresses, totals) |
| `DELETE` | `/orders/{order_id}` | Cancel/delete an order |
| `GET` | `/orders/{order_id}/items` | List line items for an order |
| `POST` | `/orders/{order_id}/items` | Add a line item to an existing order |
| `GET` | `/orders/{order_id}/items/{item_id}`| Get a single line item |
| `PATCH` | `/orders/{order_id}/items/{item_id}`| Update item quantity or pricing |
| `DELETE` | `/orders/{order_id}/items/{item_id}`| Delete a line item from an order |

---

## 1. Create Order (Checkout Directly)

```http
POST /orders
Content-Type: application/json
```

### Request Body:
```json
{
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "shipping_address_id": 1,
  "billing_address_id": 1,
  "discount_amount": "5.00",
  "tax_amount": "3.50",
  "shipping_amount": "10.00",
  "status": "pending",
  "payment_status": "pending",
  "items": [
    {
      "product_id": 4,
      "quantity": 2
    }
  ]
}
```

### Example:
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
    "discount_amount": "5.00",
    "tax_amount": "3.50",
    "shipping_amount": "10.00",
    "items": [
      {
        "product_id": 4,
        "quantity": 2
      }
    ]
  }'
```

### Response (201 Created):
```json
{
  "id": 101,
  "order_number": "ORD-20260919143000-8F3E21",
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "shipping_address_id": null,
  "billing_address_id": null,
  "subtotal": "80.00",
  "discount_amount": "5.00",
  "tax_amount": "3.50",
  "shipping_amount": "10.00",
  "total_amount": "88.50",
  "status": "pending",
  "payment_status": "pending",
  "placed_at": null,
  "created_at": "2026-09-19T14:30:00Z",
  "updated_at": "2026-09-19T14:30:00Z",
  "items": [
    {
      "id": 1,
      "order_id": 101,
      "product_id": 4,
      "product_name": "Wireless Noise Cancelling Headphones",
      "sku": "HEADPHONES-001",
      "quantity": 2,
      "unit_price": "40.00",
      "total_price": "80.00",
      "created_at": "2026-09-19T14:30:00Z"
    }
  ]
}
```

---

## 2. Checkout From Active Cart (One-Click)

Converts the user's active shopping cart items into a newly placed order and marks the cart as converted.

```http
POST /orders/from-cart/{user_id}
```

### Example:
```bash
curl -X POST http://localhost:8000/orders/from-cart/TN123e4567-e89b-12d3-a456-426614174000
```

### Response (201 Created):
```json
{
  "id": 102,
  "order_number": "ORD-20260919143512-4B9F10",
  "user_id": "TN123e4567-e89b-12d3-a456-426614174000",
  "shipping_address_id": null,
  "billing_address_id": null,
  "subtotal": "120.00",
  "discount_amount": "0.00",
  "tax_amount": "0.00",
  "shipping_amount": "0.00",
  "total_amount": "120.00",
  "status": "pending",
  "payment_status": "pending",
  "placed_at": null,
  "created_at": "2026-09-19T14:35:12Z",
  "updated_at": "2026-09-19T14:35:12Z",
  "items": [
    {
      "id": 2,
      "order_id": 102,
      "product_id": 4,
      "product_name": "Wireless Noise Cancelling Headphones",
      "sku": "HEADPHONES-001",
      "quantity": 3,
      "unit_price": "40.00",
      "total_price": "120.00",
      "created_at": "2026-09-19T14:35:12Z"
    }
  ]
}
```

---

## 3. Get User Order History

Use this on the customer "My Orders" account page.

```http
GET /orders/user/{user_id}
```

### Example:
```bash
curl http://localhost:8000/orders/user/TN123e4567-e89b-12d3-a456-426614174000
```

---

## 4. Track Order by Order Number

Use this on the "Order Confirmation" and "Track Order" pages.

```http
GET /orders/number/{order_number}
```

### Example:
```bash
curl http://localhost:8000/orders/number/ORD-20260919143000-8F3E21
```

---

## 5. Update Order (Status, Payment, or Address)

```http
PATCH /orders/{order_id}
Content-Type: application/json
```

### Example payload:
```json
{
  "status": "placed",
  "payment_status": "paid"
}
```

### Example:
```bash
curl -X PATCH http://localhost:8000/orders/101 \
  -H "Content-Type: application/json" \
  -d '{"status": "placed", "payment_status": "paid"}'
```

---

## 6. Order Items Management

### Add Item to Existing Order:
```bash
curl -X POST http://localhost:8000/orders/101/items \
  -H "Content-Type: application/json" \
  -d '{"product_id": 5, "quantity": 1}'
```

### Update Item Quantity:
```bash
curl -X PATCH http://localhost:8000/orders/101/items/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3}'
```

### Remove Item from Order:
```bash
curl -X DELETE http://localhost:8000/orders/101/items/1
```

---

## Frontend Integration Examples (JavaScript / TypeScript)

### 1. Complete Checkout Flow (Cart to Order)

```javascript
const API_BASE = 'http://localhost:8000';

export async function checkoutActiveCart(userId) {
  // 1. Convert active cart to order
  const response = await fetch(`${API_BASE}/orders/from-cart/${userId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Checkout failed');
  }

  const order = await response.json();
  console.log('Order created successfully:', order.order_number);
  return order;
}
```

### 2. Confirm Order Placement & Payment

```javascript
export async function confirmOrderPlaced(orderId) {
  const response = await fetch(`${API_BASE}/orders/${orderId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      status: 'placed',
      payment_status: 'paid'
    }),
  });

  return await response.json();
}
```

### 3. Load Customer Order History

```javascript
export async function fetchUserOrders(userId) {
  const response = await fetch(`${API_BASE}/orders/user/${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user order history');
  }
  return await response.json();
}
```

### 4. Search / Track Order by Order Number

```javascript
export async function trackOrder(orderNumber) {
  const response = await fetch(`${API_BASE}/orders/number/${encodeURIComponent(orderNumber)}`);
  if (response.status === 404) {
    return null; // Order not found
  }
  return await response.json();
}
```

---

## Status Reference

### Order Status (`status`)
- `"pending"` — Order created, awaiting user payment / confirmation.
- `"placed"` — Customer confirmed order; `placed_at` timestamp recorded.
- `"processing"` — Warehouse is packing items.
- `"shipped"` — Order handed over to courier.
- `"delivered"` — Package received by customer.
- `"cancelled"` — Order cancelled.

### Payment Status (`payment_status`)
- `"pending"` — Payment not yet captured.
- `"paid"` — Payment successfully processed.
- `"failed"` — Transaction failed.
- `"refunded"` — Amount refunded.
