from pydantic import BaseModel
from typing import List


class CreateHooper(BaseModel):
	name: str


class CreateCommand(BaseModel):
	name: str
	hooper_name: str


class CreateLocation(BaseModel):
	latitude: float
	longitude: float


class CreateConference(BaseModel):
	name: str
	location: CreateLocation
	commands: List[CreateCommand] = []
