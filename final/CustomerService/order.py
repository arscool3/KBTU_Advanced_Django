from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
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


# customer can see history, create order, order_detail,
@router.post("")
def create_order(db: db_dependency, order: schemas.CreateOrder):
    try:
        db.add(models.Order(**order.model_dump(), total=1000))
        return {'message': 'order is created!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'error: {e}')


# -> list[Order] | dict

@router.get("/{customer_id}")
def history_order(db: db_dependency, customer_id: str):
    try:
        orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).first()
        if not orders:
            return {"message": "orders not found!"}
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@router.get("/{order_id}")
def order_detail(db: db_dependency, order_id: str):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            return {'message': 'Order not found!'}
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {e}')
