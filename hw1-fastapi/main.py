from datetime import datetime
from typing import Optional

from starlette import status
from starlette.responses import JSONResponse

import fake_db
from fastapi import FastAPI
from films.schemas import CreateFilm, Film


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/films")
async def get_films(rating: Optional[int] = None):
    if rating:
        return [film for film in fake_db.films if film.rating == rating]

    return fake_db.films


@app.get("/films/{id}")
async def get_film(id: int):
    return fake_db.films[id - 1]


@app.post("/films")
async def get_film(film: CreateFilm):
    new_id = len(fake_db.films) + 1
    new_film = Film(id=new_id, **film.dict(), release_date=datetime.now())
    fake_db.films.append(new_film)

    return new_film
