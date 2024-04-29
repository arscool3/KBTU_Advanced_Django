from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .dependencies import jwt_authentication
from .schemas import UserInSchema
from .security import register_user, login_user

__all__ = (
    "router",
)

from .services import get_user_tracking_history, get_region_by_name, get_traffic_for_region

router = APIRouter(prefix="/api/v1")


@router.post("/auth/register/", tags=["auth"])
async def register(user: UserInSchema):
    token = register_user(user.login, user.password)
    return JSONResponse(content={"token": token})


@router.post("/auth/login/", tags=["auth"])
async def login(user: UserInSchema):
    token = login_user(user.login, user.password)
    return JSONResponse(content={"token": token})


@router.get("/user/location-history/", tags=["user"])
async def get_user(
        user=Depends(jwt_authentication)
):
    history_list = await get_user_tracking_history(user_id=user.id)
    return history_list


@router.get("/traffic/", tags=["traffic"])
async def get_traffic_for_region_route(region=Depends(get_region_by_name)):
    roads = await get_traffic_for_region(region)
    return roads
