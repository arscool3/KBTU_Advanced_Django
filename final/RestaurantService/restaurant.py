from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import database as db

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


@router.get("/orders")
async def get_orders(status: str, db: db_dependency):
    pass


@router.post("/orders/status/{id}")
async def deny_order(id: str, action: str):
    pass


@router.patch("/menu_item")
async def add_menu_item():
    pass