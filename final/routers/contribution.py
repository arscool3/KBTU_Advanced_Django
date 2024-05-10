from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas import KafkaRequest
from database import session
from producer import produce

router = APIRouter(prefix='/contributions', tags=['contribution'])


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.patch('/contribute/{project_id}/{user_id}')
def contribute_to_project(project_id: int, user_id: int):
    try:
        body = KafkaRequest(project_id=project_id, user_id=user_id)
        produce(body)

        return {'message': 'contribution accepted! You can develop the project further!'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='could not contribute to project')
