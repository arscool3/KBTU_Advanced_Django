from typing import Optional

from fastapi import FastAPI

from films import database
from films.schemas import AddFilm, Film

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/films")
async def get_films(rating: Optional[int] = None):
    if rating:
        return [f for f in database.films if f.rating == rating]
    return database.films


@app.get("/films/{id}")
async def get_film(id: int):
    return database.films[id-1]

@app.post("/films")
async def add_film(film: AddFilm):
    id = len(database.films) + 1
    new_film = Film(id=id, **film.dict())
    database.films.append(new_film)
    return new_film
