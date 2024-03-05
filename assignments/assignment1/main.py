from typing import List, Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    rating: float
    director: str = Field(max_length=100)


films = []


@app.get("/films")
def get_films() -> List[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id(id: int) -> Film:
    return films[id]


@app.post("/films")
def create_film(film: Film) -> str:
    films.append(film)
    return "Film added!"


@app.get("/films/{rating}")
def get_film_rating(rating: float) -> List[Film]:
    return [film for film in films if film.rating == rating]
