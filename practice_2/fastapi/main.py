from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title='Movie App'
)

class Movie(BaseModel):
    name: str
    description: str
    rating: float = Field(ge=0, le=10)
    director: str

movies : Movie = []

@app.get('/movies/{movie_id}')
def get_movie(movie_id: int) -> Movie:
    return movies[movie_id]

@app.get('/movies')
def get_all_movies() -> list[Movie]:
    return movies

@app.get('/movies/rating/{rating}')
def get_rating(rating: float) -> list[Movie]:
    return sorted([i for i in movies if i.rating >= rating], key=lambda f : f.rating)

@app.post("/addMovies")
def addMovie(movie: Movie) -> str:
    movies.append(movie)
    return "Movie was added"    