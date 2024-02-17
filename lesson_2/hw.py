from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

films = []


class Film(BaseModel):
    name: str = Field(max_length=10)
    description: str = Field(max_length=1000)
    rating: float = Field(gt=0, lt=100)
    director: str = Field(max_length=10)


@app.get("/films")
def get_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id(id: Annotated[int, Path(ge=0)]) -> Film:
    return films[id]


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)
    return "Film was added"


@app.get("/films_by_rating/")
def get_films_by_rating(rating: Annotated[float, Query(gt=0, lt=100)]) -> list[Film]:
    return [film for film in films if films.rating == rating]
