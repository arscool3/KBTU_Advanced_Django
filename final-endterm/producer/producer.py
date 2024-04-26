import os
import pickle
import time
import logging
import random

import confluent_kafka

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

logger.info("START")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
topic = os.environ.get("DEFAULT_TOPIC", "traffic_data")

logger.info(f"{KAFKA_BOOTSTRAP}, {topic}")

producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})
logger.info("CONNECTED")
logger.info(producer)

user_id = random.randint(1, 100)


def get_person_traffic_data() -> dict:
    return {
        "person_id": user_id,
        "traffic_data": {
            "timestamp": time.time(),
            "location": {
                "latitude": round(random.uniform(0, 100), 5),
                "longitude": round(random.uniform(0, 100), 5),
            },
            "speed": random.randint(0, 100),
            "acceleration": round(random.uniform(0, 100), 3),
            "direction": random.randint(0, 360),
        },
    }


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


def producer():
    while True:
        try:
            time.sleep(1)
            traffic_data = get_person_traffic_data()
            produce(traffic_data)
            logger.info(f"{time.time()}-PRODUCED")
        except Exception as e:
            logger.warning(f"Error: {e}")


if __name__ == "__main__":
    producer()
