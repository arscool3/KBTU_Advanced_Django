#1Practice Task: Building Basic Web App With FastApi
#Objective:
#To develop Basic FastApi Application (4 endpoints)
#1) List All Films
#2) Get Film by Id
#3) Add Film (name, description, rating, director)
#4) Get Film by rating
#1. 2. 3. 4.
#Use FastApi
#Type Hinting (Example :int, :str)
#Pydantic
#Filters
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

films = ["emma," "pride and prejudice", "little women"]

class Film(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=15)
    description: str = Field(max_length=200)
    rating:int = Field (gt=0, ls=10)


@app.get("/films")
def get_films() -> list[Film]
   return films

@app.get("/films/{id}")
def get_fimls_byid(id: Annotated[int, Path(ge=0)]) -> Film:
    return films[id]


@app.post("/films")
def add_film(film: Film) -> str:
    films.append(film)
    return "film was added"

@app.get("/films_by_rating")
def get_by_rating(rating: Annotated[int, Query(gt=0, lt=10)]) -> list[Film]:
    return [film for film in films if film.rating == rating]





