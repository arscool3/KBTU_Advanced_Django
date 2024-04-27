import logging
import pickle
import time

import confluent_kafka
from .get_traffic_data import get_person_traffic_data
from ..settings import KAFKA_BOOTSTRAP, TOPIC

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

__all__ = ["producer_loop"]


def produce(res: dict, producer: confluent_kafka.Producer) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=TOPIC, value=to_send)
    producer.flush()


def producer_loop():
    logger.info("START")
    producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})
    logger.info("CONNECTED")

    while True:
        try:
            time.sleep(1)
            traffic_data = get_person_traffic_data()
            produce(traffic_data, producer=producer)
            logger.info(f"{time.time()}-PRODUCED")
        except Exception as e:
            logger.warning(f"Error: {e}")
