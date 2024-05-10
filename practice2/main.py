from fastapi import FastAPI, Path, Query
from pydantic import BaseModel  # serializing and deserializing
from typing import Annotated

app = FastAPI()


class Film(BaseModel):
    id: int
    name: str
    description: str
    rating: float
    director: str


films = []


@app.get("/films")
def list_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id(id: Annotated[int, Path(gte=0)]) -> Film:
    return films[id]


@app.post("/films")
def add_film(f: Film) -> str:
    films.append(f)
    return f"Film id added"

@app.get("/films_by_rating/")
def get_students_by_rating(rating: Annotated[int, Query(gte=0, lte=10)]) -> list[Film]:
    return [f for f in films if f.rating == rating]
