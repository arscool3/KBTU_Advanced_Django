from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session, get_db
from schemas import *
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


# def get_db():
#     try:
#         yield session
#         session.commit()
#     except:
#         raise
#     finally:
#         session.close()
#

@app.post('/genre')
def add_genre(genre: CreateGenre, session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**genre.model_dump()))
    return genre.name


@app.get("/genre")
def get_genres(session: Session = Depends(get_db)) -> list[Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres


@app.post('/director')
def add_director(director: CreateDirector, session: Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return director.name


@app.get("/director")
def get_directors(session: Session = Depends(get_db)) -> list[Director]:
    db_directors = session.execute(select(db.Director)).scalars().all()
    directors = [Director.model_validate(db_director) for db_director in db_directors]
    return directors


@app.post('/film')
def add_film(film: CreateMovie, session: Session = Depends(get_db)):
    session.add(db.Film(**film.model_dump()))
    return film.name


@app.get("/film")
def get_film(session: Session = Depends(get_db)) -> list[Film]:
    db_films = session.execute(select(db.Film)).scalars().all()
    films = [Film.model_validate(db_film) for db_film in db_films]
    return films
