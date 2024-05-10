from sqlalchemy.orm import Session
from .base import Base
from .session import engine, SessionLocal
from ..models import User, Product, Order, OrderItem, Inventory, Notification

def create_tables():
    Base.metadata.create_all(bind=engine)

def initial_data():
    db = SessionLocal()
    try:
        user1 = User(username='john_doe', email='john.doe@example.com', hashed_password='hashed_pwd')
        user2 = User(username='jane_doe', email='jane.doe@example.com', hashed_password='hashed_pwd')
        db.add(user1)
        db.add(user2)

        product1 = Product(name="Laptop", description="High performance laptop", price=1000.0)
        product2 = Product(name="Smartphone", description="Latest model smartphone", price=700.0)
        db.add(product1)
        db.add(product2)

        db.commit()

        order = Order(user_id=user1.id)
        db.add(order)
        db.commit()

        item1 = OrderItem(order_id=order.id, product_id=product1.id, quantity=1, price=product1.price)
        item2 = OrderItem(order_id=order.id, product_id=product2.id, quantity=2, price=product2.price)
        db.add(item1)
        db.add(item2)
        
        inventory1 = Inventory(product_id=product1.id, quantity=50)
        inventory2 = Inventory(product_id=product2.id, quantity=100)
        db.add(inventory1)
        db.add(inventory2)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    initial_data()
