from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.settings import settings
from app.routes.auth_routes import router as auth_router
from app.routes.category_routes import router as category_router
from app.routes.product_routes import router as product_router
from app.routes.search_routes import router as search_router
from app.routes.sub_category_routes import router as subcategory_router
from app.routes.user_routes import router as user_router

app = FastAPI(title="Ecommerce Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(product_router)
app.include_router(search_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Ecommerce Backend"}
