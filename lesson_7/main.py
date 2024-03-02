from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session as db_session
from schemas import CreateGenre, Genre, CreateDirector, CreateMovie, Movie
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
    session = db_session()
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


@app.post("/director")
def create_director(director: CreateDirector, session: Session = Depends(get_db)):
    session.add(db.Director(**director.model_dump()))
    return director


@app.get("/directors")
def get_directors(session: Session = Depends(get_db)) -> list[Genre]:
    directors = session.execute(select(db.Director)).scalars().all()
    genres = [Genre.model_validate(director) for director in directors]
    return genres


@app.post("/film")
def create_film(film: CreateMovie, session: Session = Depends(get_db)):
    session.add(db.Film(**film.model_dump()))
    return film


@app.get("/films")
def get_film(session: Session = Depends(get_db)):
    films = session.execute(select(db.Film)).scalars().all()
    return [Movie.model_validate(film) for film in films]
