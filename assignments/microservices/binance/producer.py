import confluent_kafka
from schemas import Binance

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "kafka:9092"}
)

topic = 'main_topic'


def produce(binance: Binance) -> None:
    producer.produce(topic, binance.model_dump_json())
    producer.flush()
