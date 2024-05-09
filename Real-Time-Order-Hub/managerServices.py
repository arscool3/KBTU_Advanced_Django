import json

from sqlalchemy.orm import sessionmaker
from database.db import engine
from models import Order, OrderItem
from datetime import datetime
from models.userModel import *

SessionLocal = sessionmaker(bind=engine)


def process_order_request(raw_data):
    db = SessionLocal()
    try:
        data = json.loads(raw_data)
        print("Converted data:", json.dumps(data, indent=4))

        if not isinstance(data, dict) or 'products' not in data or 'chat_id' not in data:
            raise ValueError("Invalid data format")

        total_price = sum(item['price'] for item in data['products'])
        chat_id = data['chat_id']

        user = db.query(User).join(UserChatID, User.name == UserChatID.username).filter(UserChatID.chat_id == chat_id).first()

        if not user:
            print("User not found")
            return

        new_order = Order(
            user_id=user.id,
            total_price=total_price,
            status='new',
            order_date=datetime.now().date(),
            delivery_address=user.address
        )
        db.add(new_order)
        db.commit()

        for item in data['products']:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['id'],
                quantity=1,
                price_per_unit=item['price']
            )
            db.add(order_item)

        db.commit()
        print(f"Processed order {new_order.id} with {len(data['products'])} items.")
    except Exception as e:
        db.rollback()
        print(f"Failed to process order: {str(e)}")
    finally:
        db.close()


def receive_kafka_message(raw_message):
    try:
        process_order_request(raw_message)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", str(e))