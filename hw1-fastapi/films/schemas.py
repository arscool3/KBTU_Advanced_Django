from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Film(BaseModel):
    id: int
    name: str
    description: str
    director: Optional[str] = None
    rating: int
    release_date: datetime


class CreateFilm(BaseModel):
    name: str
    description: str
    director: str
    rating: int

