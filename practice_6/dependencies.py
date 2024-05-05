from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from models import Film, Genre, Director, Actor, User
from database import SessionLocal

def get_db() -> Session:   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(user_id: int, db: Session = Depends(get_db)) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_genre(genre_id: int, db: Session = Depends(get_db)) -> Optional[Genre]:
    return db.query(Genre).filter(Genre.id == genre_id).first()

def get_director(director_id: int, db: Session = Depends(get_db)) -> Optional[Director]:
    return db.query(Director).filter(Director.id == director_id).first()

def get_actor(actor_id: int, db: Session = Depends(get_db)) -> Optional[Actor]:
    return db.query(Actor).filter(Actor.id == actor_id).first()

def get_film(film_id: int, db: Session = Depends(get_db)) -> Optional[Film]:
    return db.query(Film).filter(Film.id == film_id).first()



UserDependency = Annotated[User, Depends(get_user)]
GenreDependency = Annotated[Genre, Depends(get_genre)]
DirectorDependency = Annotated[Director, Depends(get_director)]
ActorDependency = Annotated[Actor, Depends(get_actor)]
FilmDependency = Annotated[Film, Depends(get_film)]

ModelUserDependency = Annotated[User, Depends(get_user)]
ModelGenreDependency = Annotated[Genre, Depends(get_genre)]
ModelDirectorDependency = Annotated[Director, Depends(get_director)]
ModelActorDependency = Annotated[Actor, Depends(get_actor)]
ModelFilmDependency = Annotated[Film, Depends(get_film)]


class UserDependencyClass:
    def __call__(self, db_user: User = Depends(get_user)) -> User | None:
        return db_user

class GenreDependencyClass:
    def __call__(self, db_genre: Genre = Depends(get_genre)) -> Genre | None:
        return db_genre

class DirectorDependencyClass:
    def __call__(self, db_director: Director = Depends(get_director)) -> Director | None:
        return db_director


class FilmDependencyClass:
    def __call__(self, db_film: Film = Depends(get_film)) -> Film | None:
        return db_film
