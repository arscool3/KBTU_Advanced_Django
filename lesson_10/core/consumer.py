import os
import pickle

from database import session, HeatMapData

import confluent_kafka

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
GROUP_ID = os.environ.get("GROUP_ID", "main_group")
MESSAGE_NUM = os.environ.get("MESSAGE_NUM", 20)

consumer = confluent_kafka.Consumer({"bootstrap.servers": KAFKA_BOOTSTRAP, "group.id": GROUP_ID})

topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

consumer.subscribe([topic])


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=MESSAGE_NUM, timeout=0.1)
            for message in messages:
                data = pickle.loads(message.value())
                db_heatmap = HeatMapData(
                    timestamp=data.get("timestamp"),
                    data=data.get("data")
                )
                session.add(db_heatmap)
            session.commit()

    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()
