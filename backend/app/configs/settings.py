import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings:
    database_url: str
    database_ssl_require: bool
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: SecretStr

    def __init__(self) -> None:
        self.database_url = os.environ["DATABASE_URL"]
        self.database_ssl_require = os.getenv("DATABASE_SSL_REQUIRE", "false").lower() == "true"
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.environ["SMTP_USER"]
        self.smtp_password = SecretStr(os.environ["SMTP_PASSWORD"])


settings = Settings()
