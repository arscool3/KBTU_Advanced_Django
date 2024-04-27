import confluent_kafka
import httpx
import pickle
import logging

from settings import KAFKA_BOOTSTRAP, GROUP_ID, TOPIC, MESSAGE_NUM, CELERY_SERVER

__all__ = ["consumer_loop"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def consumer_loop():
    logger.info("Starting consumer loop")
    consumer_data = {"bootstrap.servers": KAFKA_BOOTSTRAP, "group.id": GROUP_ID}
    try:
        consumer = confluent_kafka.Consumer(
            consumer_data
        )
        consumer.subscribe([TOPIC])
        logger.info(f"Subscribed to {TOPIC} and connected")

        while True:
            consume_message(consumer)
            logger.info("Consumed messages")

    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


def consume_message(consumer):
    messages = consumer.consume(num_messages=MESSAGE_NUM, timeout=0.1)
    for message in messages:
        try:
            data = pickle.loads(message.value())
            response = httpx.post(f"{CELERY_SERVER}/calculate/", json=data)
        except Exception as e:
            logger.warning(f"Failed to process message: {e}, data {message.value().decode('UTF-8')}")
        else:
            try:
                response.raise_for_status()
            except Exception as e:
                logger.warning(f"Failed to process message: {e}")
