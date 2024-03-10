from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Optional
from pydantic.types import  conint


class FilmBase(BaseModel):
    name: str
    description: str
    rating: int
    director: str


class FilmCreate(FilmBase):
    pass


