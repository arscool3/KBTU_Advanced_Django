from fastapi import APIRouter

from app.api.user_api import router as user_router
from app.api.product_api import router as product_router
from app.api.order_api import router as order_router
from app.api.inventory_api import router as inventory_router
from app.api.notification_api import router as notification_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
api_router.include_router(notification_router, prefix="/notifications", tags=["notifications"])
