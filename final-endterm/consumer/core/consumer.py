import confluent_kafka
import pickle
import logging

from settings import KAFKA_BOOTSTRAP, GROUP_ID, TOPIC, MESSAGE_NUM, CELERY_SERVER
from .celery_broker import celery_app

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
    messages = consumer.consume(num_messages=MESSAGE_NUM)
    logger.info(f"consumed messages {messages}")
    for message in messages:
        try:
            data = pickle.loads(message.value())
            # response = httpx.post(f"{CELERY_SERVER}/calculate/", json=data)
            result = celery_app.send_task("calculate_traffic_task", args=[data], queue="calculations")
        except Exception as e:
            try:
                logger.warning(f"Failed to process message: {e}, data {message.value().decode('UTF-8')}")
            except:
                logger.warning(f"Failed to process message: {e}")
        else:
            try:
                logger.info(f"Sent message to Celery: {result.id}")
                # response.raise_for_status()
            except Exception as e:
                logger.warning(f"Failed to process message: {e}")
