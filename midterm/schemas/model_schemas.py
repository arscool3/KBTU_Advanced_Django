from pydantic import BaseModel


class IdBaseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Song(IdBaseModel):
    name: str
    filename: str
    lyrics: str


class Artist(IdBaseModel):
    name: str


class Album(IdBaseModel):
    songs: list[Song]
    artists: Artist


class Product(IdBaseModel):
    name: str
    description: str
    price: float
    artist: Artist


class Location(IdBaseModel):
    latitude: float
    longitude: float


class Concert(IdBaseModel):
    name: str
    location: Location
    artist: Artist
