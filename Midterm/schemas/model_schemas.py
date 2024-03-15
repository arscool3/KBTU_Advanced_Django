from pydantic import BaseModel


class IdBaseModel(BaseModel):
	id: int

	class Config:
		from_attributes = True


class Command(IdBaseModel):
	name: str
	description: str
	conference_id: int
	hooper_id: int


class Hooper(IdBaseModel):
	name: str
	commands: list[Command] = []


class Location(IdBaseModel):
	latitude: float
	longitude: float


class Conference(IdBaseModel):
	name: str
	location: Location
	commands: list[Command] = []
