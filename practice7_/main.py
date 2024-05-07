
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session
from schemas import CreateGenre, Genre,CreateMovie,Movie,Director,CreateDirector
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

@app.post('/movie')
def add_movie(movie: CreateMovie, session: Session = Depends(get_db)) -> str:
    session.add(db.Movie(**movie.model_dump()))
    return movie.name


@app.get("/movie")
def get_movies(session: Session = Depends(get_db)) -> list[Movie]:
    db_movies = session.execute(select(db.Movie)).scalars().all()
    movies = [Movie.model_validate(db_movie) for db_movie in db_movies]
    return movies



@app.post('/director')
def add_director(director: CreateDirector, session: Session = Depends(get_db)) -> str:
    session.add(db.Director(**director.model_dump()))
    return director.name


@app.get("/director")
def get_directors(session: Session = Depends(get_db)) -> list[Director]:
    db_directors = session.execute(select(db.Director)).scalars().all()
    directors = [Genre.model_validate(db_director) for db_director in db_directors]
    return directors