from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title = "FilmUP"
)

class movie(BaseModel):
    id: int
    name: str
    description: str
    rating: float = Field(ge=0, le=10)
    director: str

movies = [
    
]

@app.get("/movies/")
def list_movies():
    return movies

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    return movies[movie_id]

@app.get("/movies/rating/{rating}")
def get_movie_rating(rating: float) -> list[movie]:
    return sorted([i for i in movies if i.rating >= rating], key=lambda m : m.rating)

@app.post("/add_movie/")
def add_movie(movie: movie) -> str:
    movies.append(movie)
    return "added"
