from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from database import session

import schemas as sch

router = APIRouter(prefix='/posts', tags=['post'])


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/')
def create_post(db: db_dependency, body: sch.CreatePostRequest):
    try:
        db.add(models.Post(**body.model_dump()))
        return {'message': 'post is created!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.get('/{id}')
def get_post(id: int, db: db_dependency):
    try:
        post = db.query(models.Post).filter_by(id=id).first()
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.get('/user/{user_id}')
def get_projects_by_user_id(user_id: int, db: db_dependency):
    try:
        posts = db.query(models.Post).filter_by(author_id=user_id).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.patch("{/id}")
def update_post_by_id(id: int, body: sch.UpdatePostRequest, db: db_dependency):
    try:
        post = db.query(models.Post).filter_by(id=id).first()

        post.title = body.title
        post.description = body.desciprion
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')