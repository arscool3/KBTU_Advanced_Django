from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import *
import models
from database import engine

app = FastAPI()


def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.post("/genre/")
def add_genre(genre: CreateGenre, db: Session = Depends(get_db)) -> str:
    db.add(models.Genre(**genre.model_dump()))
    return genre.name


@app.get("/genre/")
def get_genre_by_ud(id: int, db: Session = Depends(get_db)) -> Genre:
    db_genre = db.get(models.Genre, id)
    genre = Genre.model_validate(db_genre)
    return genre
