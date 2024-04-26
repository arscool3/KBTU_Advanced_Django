import os
import pickle
import time

import confluent_kafka
import httpx

print("\n\n\n\n\nSTART\n\n\n\n")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")

producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})

topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

print("\n\n\n\n\nCONNECTED\n\n\n\n")


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


if __name__ == "__main__":
    while True:
        time.sleep(5)
        # produce({})
        print("Produced")
