import os
import pickle

import confluent_kafka
import httpx

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
GROUP_ID = os.environ.get("GROUP_ID", "main_group")
MESSAGE_NUM = os.environ.get("MESSAGE_NUM", 1)
TOPIC = os.environ.get("DEFAULT_TOPIC", "traffic_data")
consumer_data = {"bootstrap.servers": KAFKA_BOOTSTRAP, "group.id": GROUP_ID}
celery_server = os.environ.get("CELERY_SERVER", "http://localhost:8888")


def consume():
    try:
        consumer = confluent_kafka.Consumer(
            consumer_data
        )
        consumer.subscribe([TOPIC])

        while True:
            consume_message(consumer)

    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


def consume_message(consumer):
    messages = consumer.consume(num_messages=MESSAGE_NUM, timeout=0.1)
    for message in messages:
        data = pickle.loads(message.value())
        response = httpx.post(f"{celery_server}/calculate/", json=data)
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    consume()
