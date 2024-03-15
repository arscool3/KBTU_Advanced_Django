from pydantic import BaseModel


class CreateArtist(BaseModel):
    name: str


class CreateSong(BaseModel):
    name: str
    artist_name: str


class CreateAlbum(BaseModel):
    name: str
    artist_name: str


class CreateLocation(BaseModel):
    latitude: float
    longitude: float


class CreateConcert(BaseModel):
    name: str
    location: CreateLocation
