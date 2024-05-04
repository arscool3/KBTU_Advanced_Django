from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional


class FromDbModel(BaseModel):
    """Base schema for models from database."""

    class Config:
        from_attributes = True


class PersonRoadOut(FromDbModel):
    """Person road schema."""

    name: str
    traffic_rate: int
    average_speed: int


class PersonOut(FromDbModel):
    """Person schema."""

    id: int
    login: str
    current_location: Optional["LocationOut"]
    current_road: Optional["PersonRoadOut"]
    current_speed: int


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

    timestamp: datetime
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


class RoadFullOut(RoadOut):
    """Road full schema."""

    start_point: LocationOut
    end_point: LocationOut
    max_speed: int
    region: RegionOut
    max_num_of_cars: int


class IdNameRoadOut(FromDbModel):
    """Id name road schema."""

    id: int
    name: str


class RegionFullOut(RegionOut):
    """Region full schema."""

    roads: list[IdNameRoadOut]
