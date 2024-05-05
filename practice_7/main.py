#add 4 testsdock
#2 for films
#2 for directors


from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session, Film, Genre, Director
from schemas import CreateGenre, Genre, CreateFilm, Film, CreateDirector, Director
import models as db

app = FastAPI()
movie_router = APIRouter(prefix='movies/')
director_router = APIRouter(prefix='directors/')

app.include_router(movie_router)
app.include_router(director_router)



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
def get_film(session:Session = Depends(get_db))->list[Film]:
    db_films = session.execute(select(db.Film)).scalars().all()
    films = [Film.model_validate(db_films) for db_film in db_films]
    return films

@app.post("/film")
def addd_film(film: CreateFilm, session:Session = Depends(get_db))->str:
    session.add(db.Film(**film.model_dump()))
    return film.name

@app.get("/director")
def get_director(session:Session = Depends(get_db))->list[Director]:
    db_directors = session.execute(select(db.Director)).scalars().all()
    directors = [Director.model_validate(db_directors) for db_director in db_directors]
    return directors

@app.post("/director")
def addd_director(director: CreateDirector, session:Session = Depends(get_db))->str:
    session.add(db.Director(**director.model_dump()))
    return director.name




