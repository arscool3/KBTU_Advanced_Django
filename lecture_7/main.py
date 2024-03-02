from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

import lecture_7.models as db
import lecture_7.schemas as sc
from lecture_7.database import engine

app = FastAPI()

movies = [
    "Citizen Kane",
    "Vertigo",
    "Oppenheimer",
    "Barbie",
    "1+1",
    "Django"
]

def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()

@app.get("/movies")
def get_movies() -> list:
    return movies

@app.post("/movies")
def add_movie(film: sc.CreateFilm, session: Session = Depends(get_db)) -> str:
    session.add(db.Film(**film.model_dump()))
    return film.name

@app.post("/genre")
def add_genre(genre: sc.CreateGenre, session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**genre.model_dump()))
    return genre.name

@app.get("/genre")
def get_genres(session: Session = Depends(get_db)) -> list[sc.Genre]:
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = [sc.Genre.model_validate(db_genre) for db_genre in db_genres]
    return genres

@app.post("/director/")
def add_director(movie: sc.CreateDirector, db: Session = Depends(get_db)) -> str:
    db.add(db.Director(**movie.model_dump()))
    return movie.name


@app.get("/director/")
def get_directors(db: Session = Depends(get_db)) -> list[sc.Director]:
    db_movies = db.execute(select(db.Director)).scalars()
    movies = []
    for db_movie in db_movies:
        movie = sc.Director.model_validate(db_movie)
        movies.append(movie)
    return movies


@app.post("/genre/")
def add_genre(genre: sc.CreateGenre, db: Session = Depends(get_db)) -> str:
    db.add(db.Genre(**genre.model_dump()))
    return genre.name


@app.get("/genre/")
def get_genres(db: Session = Depends(get_db)) -> list[sc.Genre]:
    db_genres = db.execute(select(db.Genre)).scalars()
    genres = []
    for db_genre in db_genres:
        genre = sc.Genre.model_validate(db_genre)
        genres.append(genre)
    return genres


@app.get("/genre/id/")
def get_genre_by_ud(id: int, db: Session = Depends(get_db)) -> sc.Genre:
    db_genre = db.get(db.Genre, id)
    genre = sc.Genre.model_validate(db_genre)
    return genre
