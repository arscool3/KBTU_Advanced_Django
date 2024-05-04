from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Film(BaseModel):
    title: str
    year: int


films = []


class FilmDep:
    def __call__(self, new_film: Film):
        films.append(new_film)
        return new_film


def add_film(film: Film):
    films.append(film)
    return film


def get_films():
    return films


@app.get("/films")
def get_films(film_list: List[Film] = Depends(get_films)):
    return film_list


@app.post("/film")
def create_film(film: Film = Depends(add_film)):
    return film


@app.post("/new_film")
def create_film(film: Film = Depends(FilmDep())):
    return film
