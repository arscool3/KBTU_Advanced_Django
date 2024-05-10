from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import select
from config import EMAIL_SERVICE
from sqlalchemy.orm import Session
from starlette import status
import models
import database as db
import schemas
import httpx
from producer import produce

router = APIRouter(
    prefix="/orders",
    tags=['order']
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


@router.post("")
async def create_order(db: db_dependency, order: schemas.CreateOrder):
    try:
        db.add(models.Order(**order.model_dump(), total=0))
        return {'message': 'order is created!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'error: {e}')


@router.get("/{order_id}")
async def detail(order_id: str, db: db_dependency):
    try:
        order = db.query(models.Order).filter_by(id=order_id).first()
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


@router.patch("/{order_id}")
async def add_order_item(order_id: str, item: schemas.CreateOrderItem, db: db_dependency) -> dict:
    try:
        restaurant_item = db.query(models.RestaurantMenuItem).filter(
            models.RestaurantMenuItem.id == item.restaurant_item_id).first()

        if not restaurant_item:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f'menu item not found by id: {item.restaurant_item_id}')

        db.add(models.OrderItem(**item.model_dump(), price=restaurant_item.price, order_id=order_id))

        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f'order not found by id: {item.order_id}')

        order.total = int(restaurant_item.price * item.quantity)

        return {'message': 'order_item is added!'}
    except Exception as e:
        HTTPException(status_code=500, detail=f'{e}')


@router.patch("/buy_order/{order_id}")
async def change_order_status(db: db_dependency, order_id: str, background_task: BackgroundTasks,
                              status_request: str = Query('PAID', enum=['PAID', 'DENY-CUSTOMER'])) -> dict:
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'order not found by id: {order_id}')

        if order.status == "PENDING" or order.status == 'PAID':
            order.status = status_request

            if order.status == "PAID":
                produce(schemas.Order.model_validate(order))
                background_task.add_task(buy_test, 'd_korganbek@kbtu.kz', '1', '1', 1000)

            return {'message': 'order successfully changed!'}
        return {'message': 'your order denied. You cant change status'}
    except Exception as e:
        HTTPException(status_code=500, detail=f'{e}')


@router.get("/history/{customer_id}")
async def history_order(db: db_dependency, customer_id: str):
    try:
        orders = db.execute(select(models.Order).filter(models.Order.customer_id == customer_id)).scalars().all()
        if not orders:
            return {"message": "orders not found!"}
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


def buy_test(email: str = 'd_korganbek@kbtu.kz', restaurant_id: str = '1', order_id: str = '1', total: int = 1000):
    url = EMAIL_SERVICE
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        'email': email,
        'username': email,
        'total': total,
        'order_id': order_id,
        'restaurant_id': restaurant_id
    }

    response = httpx.post(url, headers=headers, json=data)
    print(response)
