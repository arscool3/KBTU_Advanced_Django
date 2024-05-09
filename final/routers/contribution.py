from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from database import session
from tasks import send_contribution_request_notification

router = APIRouter(prefix='/contributions', tags=['contribution'])


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.patch('/contribute/{project_id}/{user_id}')
def contribute_to_project(project_id: int, user_id: int, db: db_dependency):
    try:
        contribution = db.query(models.Contribution).filter_by(project_id=project_id).first()

        send_contribution_request_notification(contribution.id, user_id, db)

        user = db.query(models.User).filter_by(id=user_id).first()
        user.contribution_id = contribution.id

        return {'message': 'contribution accepted! You can develop the project further!'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='could not contribute to project')