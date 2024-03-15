from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
    rating: float = Field(default=0.0, gt=1.0, lt=5.0)
    director: str


films = []


@app.get("/films")
def get_films():
    return films


@app.get("/films/{id}")
def get_film_by_id(id: int):
    return films[id]


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)

    return "Film is added successfully!"


@app.get("/films")
def get_film_rating(rating: Annotated[float, Query(gt=0.0, lt=5.0)]) -> list[Film]:
    return [f for f in films if f.rating == rating]
