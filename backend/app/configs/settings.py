import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings:
    database_url: str
    database_ssl_require: bool
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: SecretStr
    spaces_access_key: str
    spaces_secret_key: str
    spaces_region: str
    spaces_bucket: str
    spaces_endpoint: str

    def __init__(self) -> None:
        self.database_url = os.environ["DATABASE_URL"]
        self.database_ssl_require = os.getenv("DATABASE_SSL_REQUIRE", "false").lower() == "true"
        self.secret_key = os.environ["SECRET_KEY"]
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.environ["SMTP_USER"]
        self.smtp_password = SecretStr(os.environ["SMTP_PASSWORD"])
        self.spaces_access_key = os.getenv("SPACES_ACCESS_KEY", "")
        self.spaces_secret_key = os.getenv("SPACES_SECRET_KEY", "")
        self.spaces_region = os.getenv("SPACES_REGION", "nyc3")
        self.spaces_bucket = os.getenv("SPACES_BUCKET", "")
        self.spaces_endpoint = os.getenv("SPACES_ENDPOINT", f"https://{self.spaces_region}.digitaloceanspaces.com")


settings = Settings()
