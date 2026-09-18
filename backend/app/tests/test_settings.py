import os

from app.configs.settings import Settings


def test_settings_accepts_legacy_space_env_names(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecomm_db")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("SMTP_USER", "test@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")
    monkeypatch.setenv("DO_SPACES_KEY", "legacy-spaces-key")
    monkeypatch.setenv("DO_SPACES_SECRET", "legacy-spaces-secret")
    monkeypatch.setenv("DO_SPACES_REGION", "nyc3")
    monkeypatch.setenv("DO_SPACES_BUCKET", "legacy-bucket")
    monkeypatch.setenv("DO_SPACES_ENDPOINT", "https://nyc3.digitaloceanspaces.com")

    settings = Settings(_env_file=None)

    assert settings.spaces_access_key == "legacy-spaces-key"
    assert settings.spaces_secret_key == "legacy-spaces-secret"
    assert settings.spaces_region == "nyc3"
    assert settings.spaces_bucket == "legacy-bucket"
    assert settings.spaces_endpoint == "https://nyc3.digitaloceanspaces.com"


def test_settings_include_localhost_dev_origins(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecomm_db")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")

    settings = Settings(_env_file=None)

    assert "http://localhost:3000" in settings.allowed_origins
    assert "http://localhost:5173" in settings.allowed_origins
    assert "http://127.0.0.1:5173" in settings.allowed_origins
