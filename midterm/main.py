from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database as db
from database import SessionLocal
from pydantic import BaseModel

app = FastAPI()

class UserBase(BaseModel):
    username: str
    mail: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True

class ActorBase(BaseModel):
    fullname: str

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        orm_mode = True

class DirectorBase(BaseModel):
    fullname: str

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True

class FilmBase(BaseModel):
    name: str
    duration: int
    year: int
    genre_id: int
    director_id: int
    actors: List[int]

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id: int

    class Config:
        orm_mode = True

class Likes(BaseModel):
    user_id: int
    film_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


class DelSession():
    def __init__(self):
        self.session = db.SessionLocal()
    def __enter__(self):
        return self.session
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

@app.post('/user', response_model=None)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = db.User(**user.dict())
    session.add(db_user)
    session.commit()
    return f"User {db_user.username} created successfully"

@app.get('/users', response_model=None)
def get_users(session: Session = Depends(get_session)):
    users = session.query(db.User).all()
    return users

@app.post('/genre', response_model=None)
def create_genre(genre: Genre, session: Session = Depends(get_session)):
    db_genre = db.Genre(**genre.dict())
    session.add(db_genre)
    session.commit()
    return f"Genre {db_genre.name} created successfully"

@app.get('/genres', response_model=None)
def get_genres(session: Session = Depends(get_session)):
    genres = session.query(db.Genre).all()
    return genres

@app.post('/actor', response_model=None)
def create_actor(actor: Actor, session: Session = Depends(get_session)):
    db_actor = db.Actor(**actor.dict())
    session.add(db_actor)
    session.commit()
    return f"Actor {db_actor.fullname} created successfully"

@app.get('/actors', response_model=None)
def get_actors(session: Session = Depends(get_session)):
    actors = session.query(db.Actor).all()
    return actors

@app.post('/director', response_model=None)
def create_director(director: Director, session: Session = Depends(get_session)):
    db_director = db.Director(**director.dict())
    session.add(db_director)
    session.commit()
    return f"Director {db_director.fullname} created successfully"

@app.get('/directors', response_model=None)
def get_directors(session: Session = Depends(get_session)):
    directors = session.query(db.Director).all()
    return directors


@app.post('/film', response_model=None)
def create_film(film: FilmCreate, session: Session = Depends(get_db)):
    # Fetch the Actor objects corresponding to the provided IDs
    actors = session.query(db.Actor).filter(db.Actor.id.in_(film.actors)).all()
    
    # Create the Film object
    db_film = db.Film(
        name=film.name,
        duration=film.duration,
        year=film.year,
        genre_id=film.genre_id,
        director_id=film.director_id,
        actors=actors  # Assign the list of Actor objects
    )
    
    # Add the Film object to the session and commit
    session.add(db_film)
    session.commit()
    
    return f"Film {db_film.name} created successfully"

@app.get('/films', response_model=None)
def get_films(session: Session = Depends(get_session)):
    films = session.query(db.Film).all()
    return films

@app.post('/like', response_model=None)
def like_film(like: Likes, session: Session = Depends(get_session)):
    db_like = db.Likes(**like.dict())
    session.add(db_like)
    session.commit()
    return f"Film liked by user {like.user_id} successfully"

@app.get('/likes/{user_id}', response_model=None)
def get_likes(user_id : int, session: Session = Depends(get_session)):
    likes = session.query(db.Likes).filter(db.User.id == user_id)
    return likes