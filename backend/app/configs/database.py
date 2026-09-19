from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.configs.settings import settings

DATABASE_URL = settings.database_url

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("postgresql://"):
    if settings.database_ssl_require is True:
        connect_args["sslmode"] = "require"
    elif settings.database_ssl_require is False:
        pass
    else:
        is_local = any(host in DATABASE_URL for host in ["localhost", "127.0.0.1", "0.0.0.0"])
        if not is_local and "sslmode" not in DATABASE_URL:
            connect_args["sslmode"] = "require"

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
