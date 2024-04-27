import os
import pickle

from database import session, HeatMapData
from datetime import datetime

import confluent_kafka

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
GROUP_ID = os.environ.get("GROUP_ID", "main_group")
MESSAGE_NUM = os.environ.get("MESSAGE_NUM", 20)
TOPIC = os.environ.get("DEFAULT_TOPIC", "main_topic")
consumer_data = {"bootstrap.servers": KAFKA_BOOTSTRAP, "group.id": GROUP_ID}


def consume():
    try:
        consumer = confluent_kafka.Consumer(
            consumer_data
        )
        consumer.subscribe([TOPIC])

        while True:
            # print("hahahahahah")
            consume_message(consumer)

    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


def consume_message(consumer):
    messages = consumer.consume(num_messages=MESSAGE_NUM, timeout=0.1)
    for message in messages:
        data = pickle.loads(message.value())
        db_heatmap = HeatMapData(
            timestamp=datetime.strptime(data.get("timestamp"), "%Y-%m-%d %H:%M:%S"),
            data=data.get("data")
        )
        print(data)
        session.add(db_heatmap)
    session.commit()


if __name__ == "__main__":
    consume()
