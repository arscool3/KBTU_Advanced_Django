import asyncio
import dependencies
import models
import schemas

from requests import JSONDecodeError
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()
bot = dependencies.get_bot()


@router.get("/{uid}/followers/")
async def fetch_target_followers(uid: str, db: Session = Depends(dependencies.get_db)):
    try:
        target = db.query(models.Target).filter(models.Target.uid == uid).first()
        if not target:
            target = models.Target(uid=uid)
            db.add(target)
        db.query(models.Follower).filter(models.Follower.target_uid == uid).delete()

        followers_list = await asyncio.to_thread(bot.followers, uid)

        for follower in followers_list:
            if follower is None or not hasattr(follower, 'user_id'):
                continue

            db_follower = models.Follower(
                uid=follower.user_id,
                profile_picture_url=follower.profile_picture_url,
                target_uid=uid,
                fetched_at=datetime.now()
            )
            db.add(db_follower)
            db.commit()

    except JSONDecodeError:
        db.rollback()
        raise HTTPException(status_code=404, detail="User not found or no content available.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Followers added successfully."}


@router.get("/{uid}/following/")
async def fetch_target_followings(uid: str, db: Session = Depends(dependencies.get_db)):
    try:
        target = db.query(models.Target).filter(models.Target.uid == uid).first()
        if not target:
            target = models.Target(uid=uid)
            db.add(target)
        db.query(models.Following).filter(models.Following.target_uid == uid).delete()

        following_list = await asyncio.to_thread(bot.followings, uid)

        for following in following_list:
            if following is None or not hasattr(following, 'user_id'):
                continue

            db_following = models.Following(
                uid=following.user_id,
                profile_picture_url=following.profile_picture_url,
                target_uid=uid,
                fetched_at=datetime.now()
            )
            db.add(db_following)
            db.commit()

    except JSONDecodeError:
        db.rollback()
        raise HTTPException(status_code=404, detail="User not found or no content available.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Following added successfully."}


@router.get("/{uid}/to_username")
async def fetch_target_username(uid: str):
    try:
        username = await asyncio.to_thread(bot.get_username, uid)
    except JSONDecodeError:
        raise HTTPException(status_code=404, detail="User not found or no content available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"username": username}


@router.get("/{username}/to_uid")
async def fetch_target_uid(username: str):
    try:
        uid = await asyncio.to_thread(bot.get_uid, username)
    except JSONDecodeError:
        raise HTTPException(status_code=404, detail="User not found or no content available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"uid": uid}


@router.get("/{uid}", response_model=schemas.Target, status_code=201)
async def create_target(uid: str, db: Session = Depends(dependencies.get_db)):
    db_target = models.Target(uid=uid)
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target


@router.get("/", response_model=list[schemas.Target])
async def read_targets(db: Session = Depends(dependencies.get_db)):
    targets = db.query(models.Target).all()
    return targets


@router.get("/{uid}", response_model=schemas.Target)
async def read_target(uid: str, db: Session = Depends(dependencies.get_db)):
    db_target = db.query(models.Target).filter(models.Target.uid == uid).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return db_target


@router.delete("/{uid}", response_model=schemas.Target)
async def delete_target(uid: str, db: Session = Depends(dependencies.get_db)):
    db_target = db.query(models.Target).filter(models.Target.uid == uid).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    db.delete(db_target)
    db.commit()
    return db_target


@router.delete("/{uid}")
async def delete_target(db: Session = Depends(dependencies.get_db)):
    db.query(models.Target).delete()
    db.commit()
    return {"message": "All targets deleted successfully."}


@router.put("/{uid}", response_model=schemas.Target)
async def update_target(uid: str, target_update: schemas.TargetUpdate, db: Session = Depends(dependencies.get_db)):
    db_target = db.query(models.Target).filter(models.Target.uid == uid).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    if target_update.uid is not None:
        db_target.uid = target_update.uid
    db.commit()
    db.refresh(db_target)
    return db_target



