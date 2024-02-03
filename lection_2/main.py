from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

films = []


class Film(BaseModel):
    title: str
    description: str
    rating: float = Field(gt=float(0), lt=float(10))
    director: str


@app.get("/films")
def get_films(page: int, limit: int) -> list[Film]:
    return films[limit * (page - 1): min(len(films), limit * page)]


@app.get("/films/{id}")
def get_films_by_id(id: Annotated[int, Path(gt=-1)]) -> Film:
    return films[id]


@app.get("/films_by_rating")
def get_films_by_age(rating: Annotated[float, Query(gt=0, lt=100)]) -> list[Film]:
    return [film for film in films if film.rating == rating]


@app.post("/films")
def add_films(film: Film) -> str:
    films.append(film)
    return "Film added"
