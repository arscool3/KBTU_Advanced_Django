from typing import List, Optional
from sqlalchemy import func
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/movies',
    tags=['Movies']
)


@router.get("/")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_film(film: schemas.FilmCreate, db: Session = Depends(get_db),):
    new_film = models.Film(**film.dict())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return new_film


@router.get("/{id}")
def get_film(id: int, db: Session = Depends(get_db)):
    film = db.query(models.Movie).filter(models.Movie.id == id).first()

    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    return film

@router.get("/{id}/rating")
def get_film_by_rating(rating: int, db: Session = Depends(get_db)):
    film = db.query(models.Movie).filter(models.Movie.rating == rating).first()

    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    return film


