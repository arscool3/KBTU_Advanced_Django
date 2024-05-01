from pydantic import BaseModel
from enum import Enum, auto


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


class User(BaseModel):
    name: str
    email: str


class SpotifyWrappedTask(BaseModel):
    id: int
    status: str

    def __init___(self, id: int, status: str):
        self.id = id
        self.status = status
