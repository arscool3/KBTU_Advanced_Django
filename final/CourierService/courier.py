from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import database as db

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

