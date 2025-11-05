from fastapi import APIRouter
from app.api.api_v1.endpoints import products, sales, init

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(init.router, prefix="/admin", tags=["admin"])
