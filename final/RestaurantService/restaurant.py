from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import database as db
import models
import schemas

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
@router.post("/menu")
async def create_menu_item(db: db_dependency, menu_item: schemas.CreateMenuItem):
    try:
        db.add(models.RestaurantMenuItem(**menu_item.model_dump()))
        return {'message': 'Menu item is added!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


# TODO update item from menu
@router.patch("/menu/{menu_item_id}")
async def update_menu_item(db: db_dependency, menu_item_id: str, menu_item_req: schemas.UpdateMenuItem):
    try:
        menu_item = db.query(models.RestaurantMenuItem).filter(models.RestaurantMenuItem.id == menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f'Menu item not found with id: {menu_item_id}')
        for key, val in menu_item_req.model_dump().items():
            setattr(menu_item, key, val)
        return menu_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


# TODO change status restaurant open/closed
@router.patch("/status/{restaurant_id}")
async def update_status_restaurant(db: db_dependency, restaurant_id: str,
                                   status_req: str = Query('CLOSE', enum=['CLOSE', 'OPEN'])):
    try:
        restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail=f'Restaurant not found with id: {restaurant_id}')
        restaurant.status = status_req
        return {'message': 'status updated successfully!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')
