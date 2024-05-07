from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import database as db
import models

router = APIRouter(
    prefix='/courier',
    tags=['courier']
)


def get_db():
    try:
        ss = db.session
        yield ss
        ss.commit()
    except Exception:
        raise
    finally:
        ss.close()


db_dependency = Annotated[Session, Depends(get_db)]


# TODO - Change status close/open
@router.patch("/status/{_id}")
async def update_courier_status(db: db_dependency, _id: str, status: str = Query('CLOSE', enum=['CLOSE', 'OPEN'])):
    try:
        courier = db.query(models.Courier).filter(models.Courier.id == _id).first()
        if not courier:
            return {'message': 'courier not found!'}
        courier.status = status
        return {'message': 'status is successfully changed!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


