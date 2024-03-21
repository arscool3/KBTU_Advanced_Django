from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session
from schemas import CreateGenre, Genre, Movie, Director, CreateMovie
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

@app.post("/films")
def add_films(film: CreateMovie, session : Session = Depends(get_db)) -> str:
    session.add(db.Film(**film.model_dump()))
    return "Film added"

@app.get("/films")
def get_films(session: Session = Depends(get_db)) -> list[Movie]:
    db_films = session.execute(select(db.Film)).scalars().all()
    films = [Movie.model_validate(db_genre) for db_genre in db_films]
    return films


@app.post("/director")
def add_director(director: Director, session : Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return "Director added"

@app.get("/director")
def get_director(session: Session = Depends(get_db)) -> list[Director]:
    db_director = session.execute(select(db.Director)).scalars().all()
    director = [Director.model_validate(db_genre) for db_genre in db_director]
    return director