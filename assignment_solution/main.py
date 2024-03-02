from typing import Annotated

from fastapi import FastAPI, Path, Query
from model import Movie


app = FastAPI()
movies = []


@app.get("/movies")
def get_movies() -> list[Movie]:
    return movies


@app.get("/movies/{id}")
def get_movie_by_id(id: Annotated[int, Path(ge=0)]) -> Movie:
    return movies[id]


@app.post("/movies")
def add_movie(movie: Movie) -> str:
    movies.append(movie)
    return "Movie was added"


@app.get("/movies_by_rating")
def get_students_by_rating(rating: Annotated[int, Query(gt=0, lt=6)]) -> list[Movie]:
    return list(filter(lambda movie: rating == movie.rating, movies))
