import dependencies
import models
import schemas

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=list[schemas.Follower])
async def read_followers(db: Session = Depends(dependencies.get_db)):
    followers = db.query(models.Follower).all()
    return followers


@router.get("/{uid}", response_model=schemas.Follower)
async def read_follower(uid: int, db: Session = Depends(dependencies.get_db)):
    db_follower = db.query(models.Follower).filter(models.Follower.uid == uid).first()
    if db_follower is None:
        raise HTTPException(status_code=404, detail="Follower not found")
    return db_follower


@router.delete("/{uid}", response_model=schemas.Follower)
async def delete_follower(uid: int, db: Session = Depends(dependencies.get_db)):
    db_follower = db.query(models.Follower).filter(models.Follower.uid == uid).first()
    if db_follower is None:
        raise HTTPException(status_code=404, detail="Follower not found")
    db.delete(db_follower)
    db.commit()
    return db_follower


@router.get("/", response_model=list[schemas.Following])
async def read_followings(db: Session = Depends(dependencies.get_db)):
    followings = db.query(models.Following).all()
    return followings


@router.get("/{uid}", response_model=schemas.Following)
async def read_following(uid: int, db: Session = Depends(dependencies.get_db)):
    db_following = db.query(models.Following).filter(models.Following.uid == uid).first()
    if db_following is None:
        raise HTTPException(status_code=404, detail="Following not found")
    return db_following


@router.delete("/{uid}", response_model=schemas.Following)
async def delete_following(uid: int, db: Session = Depends(dependencies.get_db)):
    db_following = db.query(models.Following).filter(models.Following.uid == uid).first()
    if db_following is None:
        raise HTTPException(status_code=404, detail="Following not found")
    db.delete(db_following)
    db.commit()
    return db_following




