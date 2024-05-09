from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

import models
from database import session

import schemas as sch

router = APIRouter(prefix='/projects', tags=['project'])


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/')
def create_project(db: db_dependency, body: sch.CreateProjectRequest):
    try:
        db.add(models.Project(**body.model_dump()))

        project = db.query(models.Project).filter_by(title=body.title).first()

        try:
            db.add(models.Contribution(project_id=project.id))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='could not create contribution for current project')

        return {'message': 'project is created!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'error {e}')


@router.get('/{id}')
def get_project(id: int, db: db_dependency):
    try:
        project = db.query(models.Project).filter_by(id=id).first()
        return project
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.get('/user/{user_id}')
def get_projects_by_user_id(user_id: int, db: db_dependency):
    try:
        projects = db.query(models.Project).filter_by(creator_id=user_id).all()
        return projects
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')


@router.patch("{/id}")
def update_project_by_id(id: int, body: sch.UpdateProjectRequest, db: db_dependency):
    try:
        project = db.query(models.Project).filter_by(id=id).first()

        project.title = body.title
        project.description = body.desciprion
        project.github_link = body.github_link
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'error {e}')
