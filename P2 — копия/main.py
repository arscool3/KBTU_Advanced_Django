from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Path, Query

app = FastAPI()

films = []

class Film(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=100)
    rating: int = Field(gt=1, lt=10)
    director: str = Field(max_length=20)


@app.get("/films")
def get_all_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_films_by_id(id: Annotated[int, Path(ge=0)]) -> Film:
    return films[id]


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)
    return "New film has been added successfully"


@app.get("/films_by_rating/")
def get_films_by_rating(rating: Annotated[int, Query(gt=1, lt=10)]) -> list[Film]:
    return [f for f in films if f.rating == rating]


