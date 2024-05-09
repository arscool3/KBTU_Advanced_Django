from copy import deepcopy
from typing import Annotated, List

from pydantic import ValidationError
from sqlalchemy import select

import database as db
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from order import router

app = FastAPI()
app.include_router(router)


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


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {'message': "I'm alive"}


@app.get("/restaurants", tags=['restaurants'])
async def list_of_restaurants(db: db_dependency):
    restaurant_db = db.execute(select(models.Restaurant)).scalars().all()
    test = deepcopy(restaurant_db)
    for t in test:
        t.id = str(t.id)
        t.status = str(t.status)
    ans = [schemas.Restaurant.model_validate(x) for x in test]
    del test
    return ans


@app.get("/foods", tags=['restaurants'])
async def list_of_foods(db: db_dependency):
    menu_items = db.execute(select(models.RestaurantMenuItem)).scalars().all()
    return menu_items


@app.get("/restaurants/{_id}", tags=['restaurants'])
async def list_of_food(_id: str, db: db_dependency):
    menu_items = db.execute(select(models.RestaurantMenuItem)).scalars().all()
    filter_items = [x for x in menu_items if str(x.restaurant_id) == _id]
    return filter_items
