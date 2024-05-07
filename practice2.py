from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class movie(BaseModel):
    id: int
    name: str
    rating: float

movies = [
    movie(id=1, name="little women", rating=8.5),
    movie(id=2, name="emma", rating=9.9),
    movie(id=3, name="pride and prejudice", rating=8.8),
]

@app.get("/movies", response_model=List[movie])
def list_movies():
    return movies

@app.get("/movies/{movie_id}", response_model=movie)
def get_movie_by_id(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="movie not found")

@app.post("/movies", response_model=movie)
def add_movie(movie: movie):
    movies.append(movie)
    return movie

@app.get("/movies/by_rating")
def get_movies_by_rating(rating: Optional[float] = None):
    if rating is None:
        return {"message": "what rating"}
    filtered_movies = [movie for movie in movies if movie.rating >= rating]
    return filtered_movies

