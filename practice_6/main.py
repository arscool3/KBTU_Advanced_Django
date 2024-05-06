
# at least 8 endpoints 
# at least 4 model   
# at least 3 relationships
# at least 1 dependency injection as class and 2 as methods

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm.session import Session

from database import session
from models import *
from schemas import ActorCreate, CreateUser, DirectorCreate, User, CreateGenre, Genre, FilmCreate, DirectorBase
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post("/films")
def add_films(film: FilmCreate, db: Session = Depends(get_db)) -> str:
    try:
        db_film = Film(**film.dict())
        db.add(db_film)
        db.commit()
        return {"message": "filmm was added ssuccesfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add film: {str(e)}"}


@app.get("/films", response_model=List[Film])
def get_films(db: Session = Depends(get_db)):
    return db.query(Film).all()


@app.post("/actors")
def add_actors(actor: ActorCreate, db: Session = Depends(get_db)) -> str:
    try:
        db_actor = Actor(**actor.model_dump())
        db.add(db_actor)
        db.commit()
        return {"message": "Actor was added successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add actor: {str(e)}"}


@app.get("/actors", response_model=List[Actor])
def get_actors(db: Session = Depends(get_db)):
    return db.query(Actor).all()


@app.post("/genres")
def add_genre(genre: CreateGenre, db: Session = Depends(get_db)) -> str:
    try:
        db_genre = Genre(**genre.dict())
        db.add(db_genre)
        db.commit()
        return {"message": "Genre was added successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add genre: {str(e)}"}


@app.get("/genres", response_model=List[Genre])
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@app.post("/directors")
def add_director(director: DirectorCreate, db: Session = Depends(get_db)) -> str:
    try:
        db_director = Director(**director.model_dump())
        db.add(db_director)
        db.commit()
        return {"message": "Director was added successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add director: {str(e)}"}


@app.get("/directors", response_model=List[Director])
def get_directors(db: Session = Depends(get_db)):
    return db.query(Director).all()


@app.post("/users")
def add_user(user: CreateUser, db: Session = Depends(get_db)) -> str:
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        return {"message": "User was added successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to add user: {str(e)}"}


@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/directors/{director_id}/films", response_model=List[Film])
def get_films_by_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return db.query(Film).filter(Film.director_id == director_id).all()


@app.get("/films/{film_id}", response_model=Film)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@app.put("/films/{film_id}")
def update_film(film_id: int, updated_film: FilmCreate, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    try:
        for key, value in updated_film.dict().items():
            setattr(film, key, value)
        db.commit()
        return {"message": "Film updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to update film: {str(e)}"}


@app.delete("/films/{film_id}")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    try:
        db.delete(film)
        db.commit()
        return {"message": "Film deleted successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to delete film: {str(e)}"}