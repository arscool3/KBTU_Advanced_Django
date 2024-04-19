import confluent_kafka
from binance.binance_api import fetch_binance_price_history

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "main_topic"


def produce(msg) -> None:
    data = fetch_binance_price_history(msg.symbol, msg.interval, msg.start, msg.end)
    for record in data:
        producer.produce(topic=topic, value=record)
        producer.flush()
