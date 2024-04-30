from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .dependencies import jwt_authentication, get_region_by_name, RegionDependency
from .schemas import UserInSchema, HistoryOut, RoadOut, TrafficHistoryOut, PersonOut, RoadFullOut, RegionFullOut
from .security import register_user, login_user

__all__ = (
    "router",
)

from . import services

router = APIRouter(prefix="/api/v1")


@router.post("/auth/register/", tags=["auth"])
async def register(user: UserInSchema) -> JSONResponse:
    token = register_user(user.login, user.password)
    return JSONResponse(content={"token": token})


@router.post("/auth/login/", tags=["auth"])
async def login(user: UserInSchema) -> JSONResponse:
    token = login_user(user.login, user.password)
    return JSONResponse(content={"token": token})


@router.get("/user/data/", tags=["user"])
async def get_user_data(
        user=Depends(jwt_authentication)
) -> PersonOut:
    user_data = await services.get_user_data(user_id=user.id)
    return user_data


@router.get("/user/location-history/", tags=["user"])
async def get_user_history(
        user=Depends(jwt_authentication)
) -> list[HistoryOut]:
    history_list = await services.get_user_tracking_history(user_id=user.id)
    return history_list


@router.get("/traffic/id/{region_id}/", tags=["traffic by ids"])
async def get_traffic_for_region(region_id: int) -> list[RoadOut]:
    roads = await services.get_traffic_for_region_by_id(region_id)
    return roads


@router.get("/traffic/id/{region_id}/{road_id}/", tags=["traffic by ids"])
async def get_traffic_for_road(road_id: int, region_id: int) -> RoadOut:
    road_traffic = await services.get_traffic_for_road_by_id(region_id, road_id)
    return road_traffic


@router.get("/traffic/id/history/{region_id}/{road_id}/", tags=["traffic by ids"])
async def get_traffic_history_for_road(road_id: int, region_id: int) -> list[TrafficHistoryOut]:
    road_traffic = await services.get_traffic_history_for_road_by_id(region_id, road_id)
    return road_traffic


@router.get("/traffic/{region_name}/", tags=["traffic by names"])
async def get_traffic_for_region(region=Depends(get_region_by_name)) -> list[RoadOut]:
    roads = await services.get_traffic_for_region(region)
    return roads


@router.get("/traffic/{region_name}/{road}/", tags=["traffic by names"])
async def get_traffic_for_road(road: str, region=Depends(get_region_by_name)) -> RoadOut:
    road_traffic = await services.get_traffic_for_road(region, road)
    return road_traffic


@router.get("/traffic/history/{region_id}/{road}/", tags=["traffic by names"])
async def get_traffic_history_for_road(road: str, region=Depends(get_region_by_name)) -> (
        list)[TrafficHistoryOut]:
    road_traffic = await services.get_traffic_history_for_road(region, road)
    return road_traffic


@router.get("/info/road/{road_id}/", tags=["infrastructure info"])
async def get_road_info(road_id: int) -> RoadFullOut:
    road = await services.get_road_info(road_id)
    return road


@router.get("/info/region/{region_id}/", tags=["infrastructure info"])
async def get_region_info(region=Depends(RegionDependency())) -> RegionFullOut:
    return RegionFullOut.from_orm(region)
