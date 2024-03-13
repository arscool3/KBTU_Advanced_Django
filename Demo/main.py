from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session
from schemas import CreateGenre, Genre, Film, Director, CreateFilm, CreateDirector
import models as db

app = FastAPI()

movies = [
    'Citizen Kane'
    'Oppenheimer'
    'Barbie',
    'Vertigo',
    'Django',
    'Space Odyssey',
    '1+1',
]


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
def get_genres(session: Session = Depends(get_db)) -> list[Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres


@app.get("/film")
def get_movies(session: Session = Depends(get_db)) -> list[Film]:
    db_movies = session.execute(select(db.Film)).scalars().all()
    movies = [Film.model_validate(db_movie) for db_movie in db_movies]
    return movies


@app.post("/film")
def add_films(film: CreateFilm, session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**film.model_dump()))
    return film.name
