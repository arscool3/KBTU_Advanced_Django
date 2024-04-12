import time

import confluent_kafka

from schemas import BinanceDeal

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "main_topic"


def produce(trade: BinanceDeal) -> None:
    time.sleep(1)
    producer.produce(topic=topic, value=trade.model_dump_json())
    print(f"trade in producer")
    producer.flush()
