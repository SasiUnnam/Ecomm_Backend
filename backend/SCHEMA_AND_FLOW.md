# Schema, Models, and User Flow

## Overview

The backend uses FastAPI, Pydantic schemas, SQLAlchemy models, and PostgreSQL. User identifiers are UUIDs generated with `uuid.uuid4`, while roles are stored as an enum directly on each user.

The first-time registration flow is email-first:

1. The user submits an email address.
2. The backend generates and emails a one-time password (OTP).
3. The user submits the OTP.
4. The backend creates a minimal, verified user record.
5. The user can add profile details later.

## Database Models

### Role enum

Defined in [app/models/role.py](app/models/role.py). Available values are:

- `super_admin`
- `team_member`
- `user`

### `users`

Defined in [app/models/user.py](app/models/user.py).

| Field | Type | Constraints / Purpose |
| --- | --- | --- |
| `id` | UUID | Primary key, generated with `uuid.uuid4` |
| `first_name` | String | Optional |
| `last_name` | String | Optional |
| `email` | String | Required and unique |
| `password_hash` | String | Optional; stored as a bcrypt hash when a password is provided |
| `role` | `role_name` enum | Required; defaults to `user` |
| `phone` | String | Optional |
| `is_active` | Boolean | Defaults to `true` |
| `email_verified` | Boolean | Defaults to `false` |
| `last_login_at` | DateTime | Optional |
| `created_at` | DateTime | Set when the record is created |
| `updated_at` | DateTime | Updated when the record changes |

Each user stores its role directly. A user created through signup receives the `user` enum value without requiring a separate role row or role-table lookup.

## Pydantic Schemas

### User schemas

Defined in [app/schemas/user.py](app/schemas/user.py).

- `UserBase`: Common user fields. Email is required; profile and role fields are optional.
- `UserCreate`: Extends `UserBase` and adds a required password for direct user creation.
- `SignupOTPRequest`: Contains only the email address used to request an OTP.
- `SignupOTPVerify`: Contains the email address and submitted OTP.
- `UserUpdate`: All profile fields are optional, allowing partial updates.
- `UserResponse`: Public user response with UUID `id` and timestamps.
- `UserInDB`: Extends `UserResponse` and includes `password_hash` for internal use.

## API Endpoints

### Request signup OTP

```http
POST /auth/signup/request-otp
```

Request:

```json
{
  "email": "new-user@example.com"
}
```

Behavior:

- Normalizes the email to lowercase.
- Rejects an email that already belongs to a user with `409`.
- Generates a six-digit OTP.
- Hashes the OTP with bcrypt before keeping it temporarily in memory.
- Sends the OTP by email.
- OTP expires after 10 minutes.

### Verify signup OTP

```http
POST /auth/signup/verify-otp
```

Request:

```json
{
  "email": "new-user@example.com",
  "otp": "123456"
}
```

Behavior:

- Checks that an OTP exists and has not expired.
- Compares the submitted OTP against the bcrypt hash.
- Creates a minimal user with the email, `email_verified=true`, `is_active=true`, and the default `user` role.
- Removes the pending OTP after successful verification.
- Returns the created user with `201`.

### List users

```http
GET /users
```

Returns the current users.

### Get one user

```http
GET /users/{user_id}
```

`user_id` must be a UUID. Returns `404` when no user is found.

### Direct user creation

```http
POST /users
```

This path accepts `UserCreate`, hashes the supplied password, and defaults the `role` field to `user` when it is omitted.

### Add or update profile details

```http
PATCH /users/{user_id}
```

`PATCH` is used because only the fields supplied by the client are changed. For example:

```json
{
  "first_name": "Alex",
  "phone": "+1-555-0100"
}
```

The endpoint also supports optional email and password updates. Email updates are checked for duplicates, and passwords are bcrypt-hashed before storage.

## Flow Diagram

```mermaid
flowchart TD
    A[Submit email] --> B[POST /auth/signup/request-otp]
    B --> C[Generate and email OTP]
    C --> D[POST /auth/signup/verify-otp]
    D --> E{OTP valid and not expired?}
    E -- No --> F[Return validation error]
    E -- Yes --> G[Create user with verified email]
    G --> H[Assign role: user]
    H --> I[Return minimal user record]
    I --> J[PATCH /users/{user_id}]
    J --> K[Add optional profile details]
```

## Supporting Utilities

- [app/utils/otp.py](app/utils/otp.py) generates cryptographically secure numeric OTPs.
- [app/utils/token.py](app/utils/token.py) contains opaque token generation and access/refresh token creation helpers. Token creation is not currently attached to the signup routes.
- [app/configs/database.py](app/configs/database.py) provides the shared SQLAlchemy `Base`, engine, and database session dependency.

## Current Database Notes

- The role enum change requires an Alembic migration to remove the old `role_id` foreign key and add the `role` enum column if the existing database still uses the roles table.
- The Alembic versions directory is currently empty, so the schema migration still needs to be created.
- Pending OTPs are currently stored in process memory. A restart clears them, and multiple application workers do not share them. Redis or a database table would be needed for durable, multi-worker OTP storage.
