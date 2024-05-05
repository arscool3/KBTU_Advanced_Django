from confluent_kafka import Producer
import api.models.models as mdl

producer = Producer(
    {"bootstrap.servers": "localhost: 9092"}
)

topic = "analys_topic"


def produce(order: mdl.Order ):
    producer.produce(topic = topic, value = order.model_dump_json())
    producer.flush()