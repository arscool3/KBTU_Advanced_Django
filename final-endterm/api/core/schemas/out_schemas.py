from pydantic import BaseModel, field_serializer
from datetime import datetime


class FromDbModel(BaseModel):
    """Base schema for models from database."""

    class Config:
        from_attributes = True


class LocationOut(FromDbModel):
    """Location schema."""

    latitude: float
    longitude: float


class HistoryOut(FromDbModel):
    """History schema."""

    timestamps: datetime
    location: LocationOut


class RegionOut(FromDbModel):
    """Region schema."""

    name: str


class TrafficHistoryOut(FromDbModel):
    """Traffic history schema."""

    timestamp: str
    average_speed: int
    traffic_rate: int


class RoadOut(FromDbModel):
    """Road schema."""

    name: str
    # traffic_history: list[TrafficHistoryOut]
    traffic_rate: int
    average_speed: int
    people: list

    @field_serializer("people")
    def serialize_num_people(self, people: list):
        return len(people)
