# Frontend API Quick Reference

Base URL: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

## Signup Flow

1. Request OTP.
2. Verify OTP.

The account is created after successful OTP verification. Profile details and the profile image can be added later, but are optional.

OTP verification creates a minimal user with `email`, `role: "user"`, `is_active: true`, and `email_verified: true`.

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/auth/signup/request-otp` | Send an OTP |
| `POST` | `/auth/signup/verify-otp` | Verify OTP and create user |
| `GET` | `/users` | List users |
| `GET` | `/users/{user_id}` | Get one user |
| `POST` | `/users` | Create user directly |
| `PATCH` | `/users/{user_id}` | Update user fields |
| `POST` | `/users/{user_id}/profile-image` | Upload one profile image |

## Request Examples

### Request OTP

```http
POST /auth/signup/request-otp
Content-Type: application/json
```

```json
{"email":"user@example.com"}
```

Response: `202 {"message":"Verification code sent"}`

### Verify OTP

```http
POST /auth/signup/verify-otp
Content-Type: application/json
```

```json
{"email":"user@example.com","otp":"123456"}
```

Response: `201` with the created user.

### Update User

```http
PATCH /users/TN<uuid>
Content-Type: application/json
```

```json
{"first_name":"Alex","last_name":"Smith","phone":"+1-555-0100"}
```

Only supplied fields are updated.

### Upload Profile Image

```http
POST /users/TN<uuid>/profile-image
Content-Type: multipart/form-data
```

The file field must be named `file`.

```javascript
const formData = new FormData();
formData.append("file", selectedFile);

await fetch(`${API_BASE_URL}/users/${userId}/profile-image`, {
  method: "POST",
  body: formData,
});
```

Do not set `Content-Type` manually when using `FormData`.

## User Response

```json
{
  "id":"TN550e8400-e29b-41d4-a716-446655440000",
  "email":"user@example.com",
  "role":"user",
  "first_name":null,
  "last_name":null,
  "phone":null,
  "profile_pic_url":null,
  "is_active":true,
  "email_verified":true,
  "last_login_at":null,
  "created_at":"2026-09-16T12:00:00",
  "updated_at":"2026-09-16T12:00:00"
}
```

`profile_pic_url` is the DigitalOcean Spaces URL; image bytes are not stored in PostgreSQL.

## Rules

- User IDs use the `TN` prefix.
- Roles are `user`, `team_member`, and `super_admin`.
- Profile images use one multipart file named `file`.
- Profile images currently have a 5 MB limit.
- Do not send `profile_pic_url`; the backend sets it after upload.
- Common errors: `400` validation, `404` not found, `409` duplicate, `413` file too large, `422` invalid input.
- JWT route authentication is not connected yet.
