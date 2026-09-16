import base64
import binascii
import uuid
from pathlib import Path
from uuid import UUID
from urllib.parse import urlparse

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, UploadFile

from app.configs.settings import settings


MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024


def get_file_url(object_key: str) -> str:
    if not object_key:
        return ""

    return (
        f"{settings.spaces_endpoint.rstrip('/')}/"
        f"{settings.spaces_bucket}/"
        f"{object_key.lstrip('/')}"
    )


def delete_file(file_url: str | None) -> None:
    if not file_url:
        return

    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.strip("/").split("/", 1)
    if len(path_parts) != 2 or path_parts[0] != settings.spaces_bucket:
        return

    client = _get_storage_client()
    try:
        client.delete_object(Bucket=settings.spaces_bucket, Key=path_parts[1])
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {exc}") from exc


def _validate_image(image_bytes: bytes, content_type: str | None) -> None:
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")
    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Image size must not exceed 5 MB")


def _get_storage_client():
    if not settings.spaces_access_key or not settings.spaces_secret_key or not settings.spaces_bucket:
        raise HTTPException(status_code=500, detail="DigitalOcean Spaces configuration is missing")

    return boto3.client(
        "s3",
        region_name=settings.spaces_region,
        aws_access_key_id=settings.spaces_access_key,
        aws_secret_access_key=settings.spaces_secret_key,
        endpoint_url=settings.spaces_endpoint,
    )


async def upload_file(file: UploadFile, folder: str) -> str:
    extension = ""
    if file.filename and "." in file.filename:
        extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}" if extension else str(uuid.uuid4())
    object_key = f"{folder}/{filename}"
    file_data = await file.read()

    client = _get_storage_client()

    try:
        client.put_object(
            Bucket=settings.spaces_bucket,
            Key=object_key,
            Body=file_data,
            ContentType=file.content_type or "application/octet-stream",
            ACL="public-read",
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {exc}") from exc

    return get_file_url(object_key)


def upload_profile_image(
    user_id: UUID,
    image_data: str | bytes,
    file_name: str | None = None,
    content_type: str | None = None,
) -> str:
    if isinstance(image_data, bytes):
        image_bytes = image_data
    else:
        try:
            clean_data = image_data.split(",", 1)[1] if "," in image_data else image_data
            image_bytes = base64.b64decode(clean_data, validate=True)
        except (ValueError, binascii.Error):
            raise HTTPException(status_code=400, detail="Invalid image data. Use a valid base64 string.")

    extension = Path(file_name or "profile.png").suffix or ".png"
    if content_type is None:
        content_type = "image/png"
    _validate_image(image_bytes, content_type)

    object_name = f"users/{user_id}{extension}"
    client = _get_storage_client()

    try:
        client.put_object(
            Bucket=settings.spaces_bucket,
            Key=object_name,
            Body=image_bytes,
            ContentType=content_type,
            ACL="public-read",
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {exc}") from exc

    return get_file_url(object_name)
