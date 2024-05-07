from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import database as db
import models

router = APIRouter(
    prefix='/restaurants',
    tags=['restaurant']
)


def get_db():
    try:
        session = db.session
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.commit()


db_dependency = Annotated[Session, Depends(get_db)]


# TODO add new item to menu
# TODO update item from menu
# TODO change status restaurant open/closed
