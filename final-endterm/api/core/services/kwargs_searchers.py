from fastapi import HTTPException
from database import session
from database.models import Region, Road, Person


async def get_road_by_kwargs(**kwargs) -> Road:
    road = session.query(Road).filter_by(**kwargs).first()

    if not road:
        raise HTTPException(status_code=404, detail="Road not found")

    return road


async def get_all_roads_by_kwargs(**kwargs) -> list[Road]:
    roads = session.query(Road).filter_by(**kwargs).all()
    return roads


async def get_region_by_kwargs(**kwargs) -> Region:
    region = session.query(Region).filter_by(**kwargs).first()

    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return region


async def get_user_by_kwargs(**kwargs) -> Person:
    user = session.query(Person).filter_by(**kwargs).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
