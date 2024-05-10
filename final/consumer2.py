from kafka import KafkaConsumer
import json
from dramatiq import pipeline
import dramatiq.middleware
from background_tasks import validate_paymant

# Add Redis middleware to Dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(redis_broker)

consumer = KafkaConsumer('payment_events', bootstrap_servers='localhost:9092', group_id='payment_group')

for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    # Enqueue background task with Dramatiq to calculate order
    validate_paymant.send(data)
    # print(order_data)

