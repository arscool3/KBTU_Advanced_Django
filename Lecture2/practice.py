from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


films = []


class Person(BaseModel):
    name: str = Field(max_length=10)


class Film(BaseModel):
    name: str = Field(max_length=10)
    description: str
    rating: int = Field(ge=0, le=5)
    director: Person


@app.get("/films/")
def get_films(page: Annotated[int, Query(gt=0)] = 1, limit: Annotated[int, Query(gt=0)] = 100) -> list[Film]:
    return films[(page - 1) * limit : min(page * limit, len(films))]


@app.post("/film/")
def add_film(film: Film) -> str:
    films.append(film)
    return "added"


@app.get("/films_by_rating/")
def get_films_by_rating(rating: int = Query(ge=0, le=5)) -> list[Film]:
    return [film for film in films if film.rating == rating]


@app.get("/film/{id}")
def get_film_by_id(id: Annotated[int, Path(ge=0)]) -> Film | str:
    try:
        return films[id]
    except:
        return "No such film"


# uvicorn practice:app --reload
