from typing import Annotated

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

films = []


class Film(BaseModel):
    name: str
    description: str
    rating: float = Field(ge=0, le=10)
    director: str = Field(max_length=20)


@app.get("/films")
def get_films() -> list[Film]:
    return films


@app.get("/films/{id}")
def get_student_by_id(id: Annotated[int, Path(ge=0)]) -> str:
    return f"Film with {id} = {films[id]}"


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)
    return "Film was added"


@app.get("/films/rating")
def get_student_by_id(rating: Annotated[int, Query(ge=0, le=10)]) -> list[Film]:
    return [film for film in films if film.rating == rating]
