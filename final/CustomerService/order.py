from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
import models
import database as db
from schemas import Order
import schemas

router = APIRouter(
    prefix="/orders",
    tags=['order']
)


# List Restaurants, ListofMenuItems, OnlyListofOneRestaurant, UpdateOrder by adding orderitem*, Buy Order*

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


@router.post("")
async def create_order(db: db_dependency, order: schemas.CreateOrder):
    try:
        db.add(models.Order(**order.model_dump(), total=0))
        return {'message': 'order is created!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'error: {e}')


@router.get("/{order_id}")
async def detail(id: str, db: db_dependency):
    order = db.query(models.Order).filter_by(id=id).first()
    return order


@router.patch("/{order_id}")
async def add_order_item(order_id: str, order_item: schemas.CreateOrderItem, db: db_dependency) -> dict:
    try:
        restaurant_item = db.query(models.RestaurantMenuItem).filter(
            models.RestaurantMenuItem.id == order_item.restaurant_item).first()

        if not restaurant_item:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f'menu item not found by id: {order_item.restaurant_item}')

        db.add(models.OrderItem(**order_item.model_dump(), price=restaurant_item.price, order_id=order_id))

        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f'order not found by id: {order_item.order_id}')

        order.total = int(restaurant_item.price * order_item.quantity)

        return {'message': 'order_item is added!'}
    except Exception as e:
        HTTPException(status_code=500, detail=f'{e}')


@router.patch("/buy_order/{order_id}")
async def change_order_status(order_id: str, status_req: str, db: db_dependency) -> dict:
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'order not found by id: {order_id}')
        order.status = status_req
        return {'message': 'order successfully changed!'}
    except Exception as e:
        HTTPException(status_code=500, detail=f'{e}')


@router.get("/{customer_id}")
async def history_order(db: db_dependency, customer_id: str):
    try:
        orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).first()
        if not orders:
            return {"message": "orders not found!"}
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
