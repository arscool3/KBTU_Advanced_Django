from typing import List
from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel, Field

app = FastAPI()

films = []


class Film(BaseModel):
    name: str = Field(max_length=10)
    description: str = Field(max_length=1000)
    rating: float = Field(gt=0, lt=100)
    director: str = Field(max_length=10)


def get_film_list() -> List[Film]:
    return films


def get_film_by_id(id: int = Path(..., ge=0)) -> Film:
    return films[id]


def add_film(film: Film) -> str:
    films.append(film)
    return "Film was added"


def get_films_by_rating(rating: float = Query(..., gt=0, lt=100)) -> List[Film]:
    return [film for film in films if film.rating == rating]


@app.get("/films")
def get_films(films: List[Film] = Depends(get_film_list)) -> List[Film]:
    return films


@app.get("/films/{id}")
def get_film_by_id_view(id: int, film: Film = Depends(get_film_by_id)) -> Film:
    return film


@app.post("/films", dependencies=[Depends(add_film)])
def add_film_view(film: Film) -> str:
    return "Film was added"


@app.get("/films_by_rating/")
def get_films_by_rating_view(films: List[Film] = Depends(get_films_by_rating)) -> List[Film]:
    return films


def get_films_by_rating(rating: float = Query(..., gt=0, lt=100)) -> List[Film]:
    return [film for film in films if film.rating == rating]


class FilmListDep:
    def __call__(self) -> List[Film]:
        return films


film_list_dep = FilmListDep()


@app.get("/films_with_class_dep/")
def get_films_with_class_dependency(films: List[Film] = Depends(film_list_dep)) -> List[Film]:
    return films
