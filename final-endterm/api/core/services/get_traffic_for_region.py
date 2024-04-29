from fastapi import HTTPException
from database import session
from database.models import Region, Road
from core.schemas import RoadOut


async def get_region_by_name(region_name: str) -> Region:
    region = session.query(Region).filter_by(name=region_name).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


async def get_traffic_for_region_by_name(region_name: str) -> list[RoadOut]:
    region = await get_region_by_name(region_name)

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    roads = session.query(Road).filter_by(region_id=region.id).all()

    return [RoadOut.from_orm(road) for road in roads]


async def get_traffic_for_region_by_id(region_id: int) -> list[RoadOut]:
    region = session.query(Region).filter_by(id=region_id).first()

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    roads = session.query(Road).filter_by(region_id=region.id).all()

    return [RoadOut.from_orm(road) for road in roads]


async def get_traffic_for_region(region: Region) -> list[RoadOut]:
    roads = session.query(Road).filter_by(region_id=region.id).all()

    return [RoadOut.from_orm(road) for road in roads]
