import json
from confluent_kafka import Consumer, KafkaError
from datetime import datetime
from algo import calculate_k_to_usd
from models import DataToHeatmap
from database import get_db
import logging


consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['main_topic'])


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consume_data():
    with get_db() as session:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                logger.info("No message received.")
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info("End of partition.")
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    break

            data = json.loads(msg.value().decode('utf-8'))
            logger.info(f"Received data: {data}")

            k_to_usd = calculate_k_to_usd(data['purchase_price'], data['sell_price'])
            logger.info(f"Calculated k_to_usd: {k_to_usd}")

            record = DataToHeatmap(
                start_time=datetime.strptime(data['start_date'], "%Y%m%d"),
                end_time=datetime.strptime(data['end_date'], "%Y%m%d"),
                k_to_usd=k_to_usd
            )

            session.add(record)
            try:
                session.commit()
                logger.info("Data committed to the database.")
            except Exception as e:
                logger.error(f"Error committing to database: {e}")
                session.rollback()



if __name__ == "__main__":
    try:
        consume_data()
    finally:
        consumer.close()
        logger.info("Consumer closed.")

