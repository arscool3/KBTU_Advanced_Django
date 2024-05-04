import json

from confluent_kafka import Producer
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from cart_item import schemas
from cart_item.models import CartItem
from product.models import Product
from repository import AbcRepository


producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'main_topic'

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

class CartItemRepo(AbcRepository):
    model = CartItem

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.CartItem.model_validate(instance)

    def create(self, body: schemas.CreateCartItem):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        product = self.session.query(Product).get(body.product_id)
        message = {
            "action": "create",
            "product_id": body.product_id,
            "product_name": product.name
        }
        producer.produce('cart_item_actions', key=str(body.product_id), value=json.dumps(message),
                         callback=delivery_report)
        producer.flush()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return instances

    def delete(self, id: int):
        cart_item = self.session.query(CartItem).options(joinedload(CartItem.product)).get(id)
        self.session.delete(cart_item)
        self.session.commit()
        message = {
            "action": "delete",
            "cart_item_id": id,
            "product_name": cart_item.product.name
        }
        producer.produce('cart_item_actions', key=str(id), value=json.dumps(message), callback=delivery_report)
        producer.flush()
        return "Deleted"