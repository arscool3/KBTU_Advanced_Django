import json
import time

import confluent_kafka

producer = confluent_kafka.Producer(
    {"bootstrap.servers": f"localhost:9092"},
)

topic = "journal_logs_topic"


def produce_journal_log(data: dict):
    try:
        producer.produce(topic=topic, value=json.dumps(data))
        producer.flush()
        print(f"Sent message: {data}")
    except Exception as e:
        print(f"Exception: {e}. DATA: {data}")
