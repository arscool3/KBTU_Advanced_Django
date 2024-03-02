from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import *
import models
from database import engine
from sqlalchemy import select

app = FastAPI()


def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.post("/movie/")
def add_movie(movie: CreateMovie, db: Session = Depends(get_db)) -> str:
    db.add(models.Movie(**movie.model_dump()))
    return movie.name


@app.get("/movie/")
def get_movies(db: Session = Depends(get_db)) -> list[Movie]:
    db_movies = db.execute(select(models.Movie)).scalars()
    movies = []
    for db_movie in db_movies:
        movie = Movie.model_validate(db_movie)
        movies.append(movie)
    return movies


@app.post("/director/")
def add_director(movie: CreateDirector, db: Session = Depends(get_db)) -> str:
    db.add(models.Director(**movie.model_dump()))
    return movie.name


@app.get("/director/")
def get_directors(db: Session = Depends(get_db)) -> list[Director]:
    db_movies = db.execute(select(models.Director)).scalars()
    movies = []
    for db_movie in db_movies:
        movie = Director.model_validate(db_movie)
        movies.append(movie)
    return movies


@app.post("/genre/")
def add_genre(genre: CreateGenre, db: Session = Depends(get_db)) -> str:
    db.add(models.Genre(**genre.model_dump()))
    return genre.name


@app.get("/genre/")
def get_genres(db: Session = Depends(get_db)) -> list[Genre]:
    db_genres = db.execute(select(models.Genre)).scalars()
    genres = []
    for db_genre in db_genres:
        genre = Genre.model_validate(db_genre)
        genres.append(genre)
    return genres


@app.get("/genre/id/")
def get_genre_by_ud(id: int, db: Session = Depends(get_db)) -> Genre:
    db_genre = db.get(models.Genre, id)
    genre = Genre.model_validate(db_genre)
    return genre
