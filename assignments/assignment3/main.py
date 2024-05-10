from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import session
from schemas import Genre, CreateGenre, Movie, CreateDirector, Director, CreateMovie
import models as db


app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.post('/genre')
def add_genre(genre: CreateGenre, session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**genre.model_dump()))
    return genre.name


@app.get("/genre")
def get_film(session: Session = Depends(get_db)) -> list[Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres


@app.post('/film')
def add_film(film: CreateMovie, session: Session = Depends(get_db)) -> str:
    session.add(db.Film(**film.model_dump()))
    return film.name


@app.get("/film")
def get_director(session: Session = Depends(get_db)) -> list[Movie]:
    db_films = session.execute(select(db.Film)).scalars().all()
    films = [Movie.model_validate(db_film) for db_film in db_films]
    return films


@app.post('/director')
def add_director(director: CreateDirector, session: Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return director.name


@app.get("/director")
def get_genres(session: Session = Depends(get_db)) -> list[Director]:
    db_director = session.execute(select(db.Director)).scalars().all()
    directors = [Director.model_validate(dir) for dir in db_director]
    return directors
