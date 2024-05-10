from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from database import session

import schemas as sch

router = APIRouter(prefix='/profiles', tags=['profile'])


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/')
def create_profile(db: db_dependency, body: sch.CreateProfileRequest):
    try:
        db.add(models.Profile(**body.model_dump()))
        return {'message': 'profile is created!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.get('/{user_id}')
def get_profile_by_user_id(user_id: int, db: db_dependency):
    try:
        profile = db.query(models.Profile).filter_by(user_id=user_id).first()
        return profile
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')