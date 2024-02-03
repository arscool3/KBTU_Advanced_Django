from typing import Annotated

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

films = []


class Film(BaseModel):
    name: str = Field()
    desc: str = Field()
    rating: float = Field(ge=0, le=10)
    director: str = Field(max_length=50)


@app.get("/films")
def get_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id(id: Annotated[int, Path(ge=0)]) -> Film:
    return films[id]


@app.get("/films_by_rating")
def get_films_by_age(rating: Annotated[float, Query(ge=0, le=10)]) -> list[Film]:
    return [film for film in films if film.rating == rating]


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)
    return "Film was added"


# uvicorn main:app --reload
