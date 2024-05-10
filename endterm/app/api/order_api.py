from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import OrderCreate, OrderOut
from ..services.order_service import OrderService

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.create_order(order.user_id, order.items)

@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    db_order = order_service.get_order_by_id(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
