from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name : str
    description: str
    rating: float = Field(ge=0, le=10)
    director: str

films : Film = []

@app.get('/films')
def allFilms() -> list[Film]:
    return films

@app.get('/films/{id}')
def filmbyId(id:int) -> Film:
    return films[id]

@app.post('/addFilm')
def addFilm(film : Film) -> str:
    films.append(film)
    return 'Success'
@app.get('/films/rating/{rating}')
def filmsByRating(rating: float) -> list[Film]:
    return sorted([i for i in films if i.rating >= rating], key=lambda f : f.rating)