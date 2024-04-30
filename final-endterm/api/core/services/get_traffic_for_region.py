from fastapi import HTTPException
from database import session
from database.models import Region, Road
from core.schemas import RoadOut, TrafficHistoryOut, RoadFullOut
from .kwargs_searchers import get_road_by_kwargs, get_region_by_kwargs, get_all_roads_by_kwargs


async def get_region_by_name(region_name: str) -> Region:
    kwargs = {"name": region_name}
    return await get_region_by_kwargs(**kwargs)


async def get_traffic_for_region_by_name(region_name: str) -> list[RoadOut]:
    region = await get_region_by_name(region_name)
    kwargs = {"region_id": region.id}

    roads = await get_all_roads_by_kwargs(**kwargs)

    return [RoadOut.from_orm(road) for road in roads]


async def get_traffic_for_region_by_id(region_id: int) -> list[RoadOut]:
    kwargs = {"region_id": region_id}

    roads = await get_all_roads_by_kwargs(**kwargs)

    return [RoadOut.from_orm(road) for road in roads]


async def get_traffic_for_region(region: Region) -> list[RoadOut]:
    kwargs = {"region_id": region.id}
    roads = await get_all_roads_by_kwargs(**kwargs)

    return [RoadOut.from_orm(road) for road in roads]


async def get_traffic_for_road(region: Region, road_name: str) -> RoadOut:
    kwargs = {"region_id": region.id, "name": road_name}
    road = await get_road_by_kwargs(**kwargs)
    return RoadOut.from_orm(road)


async def get_traffic_for_road_by_id(region_id: int, road_id: int) -> RoadOut:
    kwargs = {"region_id": region_id, "id": road_id}
    road = await get_road_by_kwargs(**kwargs)

    return RoadOut.from_orm(road)


async def get_traffic_history_for_road(region: Region, road_name: str) -> list[TrafficHistoryOut]:
    kwargs = {"region_id": region.id, "name": road_name}
    road = await get_road_by_kwargs(**kwargs)

    return [TrafficHistoryOut.from_orm(history) for history in road.history]


async def get_traffic_history_for_road_by_id(region_id: int, road_id: int) -> list[TrafficHistoryOut]:
    kwargs = {"region_id": region_id, "id": road_id}
    road = await get_road_by_kwargs(**kwargs)

    return [TrafficHistoryOut.from_orm(history) for history in road.history]


async def get_road_info(road_id: int) -> RoadFullOut:
    kwargs = {"id": road_id}
    road = await get_road_by_kwargs(**kwargs)

    return RoadFullOut.from_orm(road)
