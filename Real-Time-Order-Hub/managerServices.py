from sqlalchemy.orm import sessionmaker, Session
from database.db import engine
from models.orderModel import *
from datetime import datetime

SessionLocal = sessionmaker(bind=engine)


def process_order_request(data):
    db = SessionLocal()
    try:

        total_price = sum(item['price'] for item in data)
        new_order = Order(
            user_id=1,
            total_price=total_price,
            status='new',
            order_date=datetime.now().date(),
            delivery_address='123 Example St'
        )
        db.add(new_order)
        db.commit()

        for item in data:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['id'],
                quantity=1,
                price_per_unit=item['price']
            )
            db.add(order_item)

        db.commit()
        print(f"Processed order {new_order.id} with {len(data)} items.")
    except Exception as e:
        db.rollback()
        print(f"Failed to process order: {str(e)}")
    finally:
        db.close()


def consume_orders():
    consumer = consumer('orders_topic', 'order_group')
    for message in consumer:
        print(f"Received message: {message.value}")
        process_order_request(message.value)


if __name__ == '__main__':
    consume_orders()
