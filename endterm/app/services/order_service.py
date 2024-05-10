from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate
from app.schemas.order_item import OrderItemCreate

class OrderService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_order(self, user_id: int, items: list[OrderItemCreate]):
        db_order = Order(user_id=user_id)
        self.db.add(db_order)
        self.db.flush()  # Flush to get the order_id for items
        for item in items:
            db_item = OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity, price=item.price)
            self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_order_by_id(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()
