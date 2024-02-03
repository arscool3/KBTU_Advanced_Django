from typing import  Annotated
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name: str = Field(max_length=15)
    description: str = Field(max_length=250)
    rating: int = Field(gt=0, lt=100)
    director: str = Field(max_length=15)


films = [
    Film(name="Movie1", description="Description1", rating=85, director="Director1"),
    Film(name="Movie2", description="Description2", rating=72, director="Director2"),
    Film(name="Movie3", description="Description3", rating=90, director="Director3"),
    Film(name="Movie4", description="Description4", rating=68, director="Director4"),
    Film(name="Movie5", description="Description5", rating=95, director="Director5"),
]


@app.get("/films")
def get_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_film(id: Annotated[int, Path(ge=-1)]) -> Film:
    return films[id]


@app.get("/films_by_rating")
def get_films_by_rating(rating: Annotated[int, Query(gt=0, lt=100)]) -> list[Film]:
    return [film for film in films if film.rating == rating]


@app.post("/films")
def add_students(film: Film) -> str:
    films.append(film)
    return "Film was added to list"


