import confluent_kafka
from schemas import Order

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "kafka:9092"}
)

topic = 'restaurant_order_topic'


def produce(order: Order) -> None:
    producer.produce(topic=topic, value=order.model_dump_json())
    producer.flush()
