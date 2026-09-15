from fastapi import FastAPI

from app.routes.user_routes import router as user_router

app = FastAPI(title="Ecommerce Backend")

app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Ecommerce Backend"}
