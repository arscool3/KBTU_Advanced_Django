from kafka import KafkaConsumer
import json
from dramatiq import pipeline
import dramatiq.middleware
from back_tasks import validate

# Add Redis middleware to Dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(redis_broker)

consumer = KafkaConsumer('new_orders', bootstrap_servers='localhost:9092', group_id='order_group')

for message in consumer:
    order_data = json.loads(message.value.decode('utf-8'))
    # Enqueue background task with Dramatiq to calculate order
    print(order_data)
    validate.send(order_data)
    # print(order_data)