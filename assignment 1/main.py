from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Annotated
app = FastAPI()

class Person(BaseModel):
    name: str
    surname: str

class Film(BaseModel):
    name: str
    description: str
    rating: float
    director: Person


films = []

@app.post("/films/")
def create_film(film: Film) -> Film:
    films.append(film)
    return film

@app.get("/films/")
def get_films(lower_rating: Annotated[float, Query(ge=0)] = 0, upper_rating: Annotated[float, Query(le=10)] = 10) -> List[Film]:
    return [film for film in films if film.rating>=lower_rating and film.rating>=upper_rating]

@app.get("/films/{film_id}")
def get_films(film_id: int) -> Film:
    return films[film_id]


