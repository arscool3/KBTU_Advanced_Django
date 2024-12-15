from typing import List, Tuple, Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name: str = Field(max_length=40)
    year: int = Field(gt=2010, lt=2024)
    rating: float = Field(gt=0, le=10)
    description: str = Field(max_length=120)
    director: str = Field(max_length=20)


films: Film = []


@app.get("/films")
def get_list_of_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id(id: int) -> Film:
    return films[id]


@app.post("/addFilm")
def add_film(film: Film) -> str:
    films.append(film)
    return "Successfully added!"


@app.get("/films/rating/{rating}")
def films_by_rating(rating: float) -> list[Film]:
    return [film for film in films if film.rating == rating]

# python3 -m uvicorn main:app --reload
