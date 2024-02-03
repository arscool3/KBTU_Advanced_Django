from typing import List, Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Film(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=300)
    director: str = Field(max_length=50)
    rating: int = Field(gt=0, le=100)


films = []

_film_rating = Annotated[int, Query(gt=0, le=100)]

@app.post('/film/')
def add_film(film: Film) -> str:
    films.append(film)
    return "Film added successfully"


@app.get('/film_by_rating')
def get_film_by_rating(rating: _film_rating) -> list[Film]:
    return [film for film in films if film.rating == rating]


@app.get('/films/')
def get_films(limit: int, page: int = Query(gt=0)) -> list[Film]:
    return films[limit * (page-1): min(len(films), limit * page)]


@app.get('/film/{id}')
def test(id: int) -> str:
    return f"Film with id {id} - {films[id]}"

# uvicorn main:app --reload


def a(a:int):
    def decorator(func):
        from datetime import datetime

        def wrapped(*args, ):
            print("Started", datetime.now(), a)
            func()
            print("Ended", datetime.now())

        return wrapped
    return decorator

# @a(a=10)
# def x():
#     for _ in range(1_000_000_000):
#         continue
#
# x()