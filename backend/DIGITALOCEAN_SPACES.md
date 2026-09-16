# DigitalOcean Spaces

This document describes the DigitalOcean Spaces setup used for user profile images and other uploaded files.

## 1. Required DigitalOcean resources

Create the following in DigitalOcean:

- A DigitalOcean Space (bucket)
- A Spaces access key
- A Spaces secret key
- Optional: a custom domain or CDN endpoint for the Space

The Space region must match the region used by the application configuration.

## 2. Environment variables

Add these values to the backend `.env` file:

```env
SPACES_ACCESS_KEY=your_spaces_access_key
SPACES_SECRET_KEY=your_spaces_secret_key
SPACES_REGION=nyc3
SPACES_BUCKET=your-space-name
SPACES_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

Do not commit `.env` or expose `SPACES_SECRET_KEY` in source code, logs, frontend code, or API responses.

### Variable reference

| Variable | Required | Description |
| --- | --- | --- |
| `SPACES_ACCESS_KEY` | Yes | DigitalOcean Spaces access key |
| `SPACES_SECRET_KEY` | Yes | DigitalOcean Spaces secret key |
| `SPACES_REGION` | Yes | Space region, for example `nyc3` |
| `SPACES_BUCKET` | Yes | Space name |
| `SPACES_ENDPOINT` | Yes | S3-compatible endpoint for the selected region |

For a Space in the `nyc3` region, the endpoint is:

```text
https://nyc3.digitaloceanspaces.com
```

Other regions must use their matching endpoint, for example:

```text
https://ams3.digitaloceanspaces.com
https://sgp1.digitaloceanspaces.com
https://fra1.digitaloceanspaces.com
```

## 3. Bucket permissions

The current upload implementation sends objects with `public-read` ACL. The bucket must therefore allow public object reads if the returned URLs are expected to work directly in a browser.

Recommended settings:

- Keep write access private and restricted to the application access key.
- Allow public read access only if profile images are intentionally public.
- Use a CDN or custom domain for production traffic when appropriate.
- Apply lifecycle rules if temporary or unused files should be deleted automatically.

If the Space is private, remove the public-read behavior and use signed URLs instead. The current `get_file_url()` helper creates a public URL and does not create a signed URL.

## 4. URL format

Object keys are converted into public URLs by `get_file_url()` in `app/utils/storage.py`:

```python
from app.utils.storage import get_file_url

file_url = get_file_url("users/example-image.png")
```

The resulting URL is:

```text
https://<region>.digitaloceanspaces.com/<bucket>/users/example-image.png
```

The helper uses these project settings:

```python
settings.spaces_endpoint
settings.spaces_bucket
```

It also removes duplicate slashes around the endpoint and object key.

## 5. Upload implementation

The storage client is created with the S3-compatible DigitalOcean endpoint:

```python
boto3.client(
    "s3",
    region_name=settings.spaces_region,
    aws_access_key_id=settings.spaces_access_key,
    aws_secret_access_key=settings.spaces_secret_key,
    endpoint_url=settings.spaces_endpoint,
)
```

The backend currently supports:

- `upload_file(file, folder)` for FastAPI `UploadFile` objects
- `upload_profile_image(user_id, image_data, file_name, content_type)` for bytes or base64 image data
- `get_file_url(object_key)` for constructing a public object URL
- `delete_file(file_url)` for removing a replaced object from the Space

Profile image uploads accept image MIME types only and are limited to 5 MB. When a profile image is replaced, the previous object is deleted after the new upload succeeds. If the new image uses the same object URL, the existing object is overwritten and is not deleted separately.

Uploaded profile images use an object key similar to:

```text
users/<user-uuid>.png
```

## 6. API upload endpoint

The user profile image endpoint is:

```http
POST /users/{user_id}/profile-image
Content-Type: multipart/form-data
```

The multipart field name must be `file`.

Example with `curl`:

```bash
curl -X POST \
  "http://localhost:8000/users/<user-id>/profile-image" \
  -F "file=@/path/to/profile.png"
```

The response contains the updated user record, including `profile_pic_url`.

## 7. Dependencies

The backend requires these packages for uploads:

```text
boto3
python-multipart
```

They are listed in `requirements.txt`.

## 8. Local verification

From the backend directory, verify that the application imports and compiles:

```bash
./venv/bin/python -m compileall -q app
```

Then start the API:

```bash
./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the Swagger UI at:

```text
http://localhost:8000/docs
```

Use `POST /users/{user_id}/profile-image` to test a real upload. Confirm that:

1. The request uses `multipart/form-data`.
2. The form field is named `file`.
3. The response contains `profile_pic_url`.
4. The returned URL opens successfully in a browser.

## 9. Common errors

### Missing configuration

Error:

```text
DigitalOcean Spaces configuration is missing
```

Check that `SPACES_ACCESS_KEY`, `SPACES_SECRET_KEY`, and `SPACES_BUCKET` are present in `.env`.

### Access denied

Check that:

- The access key belongs to DigitalOcean Spaces.
- The key has access to the selected Space.
- `SPACES_REGION` and `SPACES_ENDPOINT` match the Space region.
- The bucket policy or object ACL permits the requested operation.

### URL does not open

Check that:

- The object was uploaded successfully.
- The generated object key is correct.
- The Space permits public reads, or replace public URLs with signed URLs.
- The endpoint does not contain the wrong region or bucket name.

## 10. Production recommendations

- Store secrets only in environment variables or a secrets manager.
- Restrict allowed upload MIME types and maximum file sizes.
- Validate image contents instead of trusting only the filename extension.
- Consider private objects and short-lived signed URLs for sensitive images.
- Consider a CDN or custom domain for public production assets.
- Move old profile images or replaced files to a cleanup workflow if they are no longer needed.
