from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session
from schemas import CreateGenre, Genre
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
        raiseus
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