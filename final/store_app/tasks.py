import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dependencies import get_db
from models import Order
import time

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def process_order(order_id):
    db = next(get_db())
    order = db.query(Order).filter(Order.id == order_id).one()
    # Simulate processing delay
    time.sleep(1)
    order.status = 'Processed'
    db.commit()
    print(f"Order {order_id} processed")
    db.close()
