import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.models  # noqa: F401 - ensure all models are registered with Base.metadata
from app.configs.database import Base, engine, get_db
from app.configs.settings import settings
from app.routes.auth_routes import router as auth_router
from app.routes.cart_routes import router as cart_router
from app.routes.category_routes import router as category_router
from app.routes.order_routes import router as order_router
from app.routes.product_routes import router as product_router
from app.routes.search_routes import router as search_router
from app.routes.sub_category_routes import router as subcategory_router
from app.routes.user_routes import router as user_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ecommerce_backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Verifying and initializing database schema...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/initialized successfully.")
    except Exception as exc:
        logger.error(f"Database schema initialization failed: {exc}", exc_info=True)
    yield


app = FastAPI(title="Ecommerce Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(search_router)
app.include_router(auth_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )
    logger.exception(f"Unhandled error handling {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )


@app.get("/")
def read_root():
    return {"message": "Welcome to Ecommerce Backend"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:
        logger.error(f"Health check failed: {exc}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "detail": str(exc),
            },
        )
