from datetime import datetime
from pydantic import BaseModel

__all__ = [
    "Road",
    "Location",
    "TrafficInnerData",
    "TrafficData",
]


class Road(BaseModel):
    name: str
    region: int
    traffic_rate: float
    start_position: int
    end_position: int

    class Config:
        from_attributes = True


class Location(BaseModel):
    latitude: float
    longitude: float


class TrafficInnerData(BaseModel):
    timestamp: datetime
    location: Location
    speed: int
    acceleration: float
    direction: int


class TrafficData(BaseModel):
    person_id: int
    traffic_data: TrafficInnerData
