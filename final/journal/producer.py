import json
import time

import confluent_kafka

from config import KAFKA_HOST, KAFKA_PORT

producer = confluent_kafka.Producer(
    {"bootstrap.servers": f"{KAFKA_HOST}:{KAFKA_PORT}"},
)

topic = "access_logs_topic"


def produce_journal_message(data: dict):
    try:
        producer.produce(topic=topic, value=json.dumps(data))
        producer.flush()
        print(f"Sent message: {data}")
    except Exception as e:
        print(f"Exception: {e}. DATA: {data}")
