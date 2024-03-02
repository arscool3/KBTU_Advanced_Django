from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

import database as db
from database import session, Genre, Film, Director
from schemas import CreateGenre, Genre, CreateDirector, Director, CreateMovie, Movie

app = FastAPI()

movies = [
    'The Citizen Kane',
    'Oppenheimer',
    'Barbie',
    'Vertigo',
    'Django',
    'Space Odyssey',
    '1+1',
]


@app.get("/movies")
def get_movies() -> list:
    return movies


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


@app.get("/genres")
def get_genres(session: Session = Depends(get_db)) -> List[Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres


@app.post('/director')
def add_director(director: CreateDirector, session: Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return director.name


@app.get('/directors')
def get_directors(session:Session = Depends(get_db)) -> List[Director]:
    db_directors = session.execute(select(db.Director)).scalars().all()
    directors = [Director.model_validate(db_director) for db_director in db_directors]
    return directors


@app.post("/film")
def create_film(film: CreateMovie, session: Session = Depends(get_db)):
    session.add(db.Film(**film.model_dump()))
    return film


@app.get("/films")
def get_film(session: Session = Depends(get_db)) -> List[Film]:
    db_films = session.execute(select(db.Film)).scalars().all()
    films = [Film.model_validate(db_film) for db_film in db_films]
    return films