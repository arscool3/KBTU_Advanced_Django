from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Director(BaseModel):
    name: str
    surname: str


class Film(BaseModel):
    name: str
    descrition: str
    rating: float = Field(gt=0, lt=10)
    director: Director

films: list[Film] = []

@app.get("/films/")
async def get_films() -> list[Film]:
    return films

@app.get('/films/{id}')
async def get_film_by_id(id: int) -> Film:
    return films[id]

@app.post('/films/add')
async def add_film(film: Film) -> str:
    films.append(film)
    return "Film was added"

@app.get("/films/rating")
async def get_films_by_rating(rating: float) -> list[Film]:
    return [film for film in films if film.rating == rating]