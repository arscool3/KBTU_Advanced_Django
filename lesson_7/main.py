from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select
from typing import List
from database import session
from schemas import CreateGenre, Genre, CreateFilm, CreateDirector, Film, Director
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


@app.post('/film')
def add_film(film: CreateFilm, session: Session = Depends(get_db)) -> str:
    session.add(db.Film(**film.model_dump()))
    return film.name


@app.post('/director')
def add_director(director: CreateDirector, session: Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return director.name


@app.get("/film")
def get_film(session: Session = Depends(get_db)):
    films = session.execute(select(db.Film)).scalars().all()
    return [Film.model_validate(film) for film in films]


@app.get("/director")
def get_film(session: Session = Depends(get_db)):
    directors = session.execute(select(db.Director)).scalars().all()
    return [Director.model_validate(director) for director in directors]



@app.get("/genre")
def get_genres(session: Session = Depends(get_db)) -> list[Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres
