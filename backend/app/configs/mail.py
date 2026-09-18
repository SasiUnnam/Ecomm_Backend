from fastapi_mail import ConnectionConfig

from app.configs.settings import settings


mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user,
    MAIL_PASSWORD=settings.smtp_password.get_secret_value() if hasattr(settings.smtp_password, "get_secret_value") else str(settings.smtp_password),
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM=settings.smtp_from,
    MAIL_FROM_NAME="Novum Cart",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)