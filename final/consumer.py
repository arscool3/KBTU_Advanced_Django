from kafka import KafkaConsumer
import json
from dramatiq import pipeline
import dramatiq.middleware
from background_tasks import calculate_order

# Add Redis middleware to Dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(redis_broker)

consumer = KafkaConsumer('order_events', bootstrap_servers='localhost:9092', group_id='order_group')

for message in consumer:
    order_data = json.loads(message.value.decode('utf-8'))
    # Enqueue background task with Dramatiq to calculate order
    calculate_order.send(order_data)
    # print(order_data)

