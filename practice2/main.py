from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Film(BaseModel):
    name: str
    description: str
    rating: float = Field(ge=0, le = 10)
    director: str 

films = []

@app.get("/films")
def getFilms() -> list[Film]:
    return films

@app.get("/films/{id}")
def getFilmsById(id: Annotated[int, Path(ge = 0)]) -> Film:
    return films[id]

@app.post("/films")
def addFilm(film: Film) -> str:
    films.append(film)
    return "Film was added"  

@app.get("/films_r/")
def getFilmsByRating() -> list[Film]:
    temp_films = films
    temp_films.sort(key=lambda f: f.rating)
    return films