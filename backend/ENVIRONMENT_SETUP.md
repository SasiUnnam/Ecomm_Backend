# Environment Setup Guide

This project loads configuration from the backend `.env` file using `pydantic-settings`.

## 1. Where to put credentials

Update values in the project root file:

- `.env`

This file is read by:

- `app/configs/settings.py`

Do not hardcode credentials inside application code.

---

## 2. Required variables

Use these keys in `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ecomm_db
DATABASE_SSL_REQUIRE=False

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

SPACES_ACCESS_KEY=your_spaces_access_key
SPACES_SECRET_KEY=your_spaces_secret_key
SPACES_REGION=nyc3
SPACES_BUCKET=your-space-name
SPACES_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

---

## 3. When to use which values

### Local development
Use:

- `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecomm_db`
- `ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]`
- local SMTP settings if testing email
- local DigitalOcean Spaces credentials if testing file upload

### Production / live deployment
Use:

- real database credentials
- a strong `SECRET_KEY`
- correct frontend domain in `ALLOWED_ORIGINS`
- real SMTP credentials
- real DigitalOcean Spaces bucket credentials

Example production CORS:

```env
ALLOWED_ORIGINS=["https://your-frontend.com","https://www.your-frontend.com"]
```

---

## 4. Legacy vs canonical names

The app supports both legacy and canonical env names for compatibility, but the project should prefer the canonical values below:

Canonical names:

- `SPACES_ACCESS_KEY`
- `SPACES_SECRET_KEY`
- `SPACES_REGION`
- `SPACES_BUCKET`
- `SPACES_ENDPOINT`

Legacy names still supported by config:

- `DO_SPACES_KEY`
- `DO_SPACES_SECRET`
- `DO_SPACES_REGION`
- `DO_SPACES_BUCKET`
- `DO_SPACES_ENDPOINT`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_S3_BUCKET`

Prefer the canonical names in new projects and new deployments.

---

## 5. What to change for real use

### Database
Replace the placeholder values in:

- `DATABASE_URL`
- optionally `DATABASE_SSL_REQUIRE`

### Security
Replace:

- `SECRET_KEY`

Use a long random value, not a simple word or default string.

### Email
Replace:

- `SMTP_USER`
- `SMTP_PASSWORD`

If using Gmail, use an App Password instead of the normal account password.

### Frontend access
Replace:

- `ALLOWED_ORIGINS`

Only allow the domains that should access the API.

### File storage
Replace:

- `SPACES_ACCESS_KEY`
- `SPACES_SECRET_KEY`
- `SPACES_BUCKET`
- `SPACES_ENDPOINT`

---

## 6. Validation / testing

A small regression check exists for settings parsing:

- `app/tests/test_settings.py`

This file verifies that:

- legacy DO_SPACES env names still work
- canonical `SPACES_*` names are accepted
- allowed origins parse correctly

To validate settings manually, run:

```bash
python3 - <<'PY'
from app.configs.settings import settings
print(settings.allowed_origins)
print(settings.spaces_access_key)
print(settings.spaces_bucket)
print(settings.spaces_endpoint)
PY
```

If the values print correctly, the env file is being loaded as expected.

---

## 7. Quick checklist before running the app

Before starting the backend, confirm:

- `.env` exists in the backend root
- all required secrets are filled in
- `DATABASE_URL` points to a real database
- `SECRET_KEY` is not left as a placeholder
- `ALLOWED_ORIGINS` includes your frontend URL
- `SPACES_*` values are valid for your DigitalOcean Space

If any value is still set to `your-...`, `example`, or `placeholder`, replace it before running the app in a real environment.
