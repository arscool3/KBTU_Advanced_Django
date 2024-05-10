import json
import models as db
import confluent_kafka
from database import get_db
from schemas import CreateLog

consumer = confluent_kafka.Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "main_group",
    }
)

topic = "logs_topic"

consumer.subscribe([topic])


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=5, timeout=1.5)
            if not messages:
                print("no upcoming messages")
            for message in messages:
                print(f"Incoming message is: {message.value()}")
                message = json.loads(message.value().decode("utf-8"))
                save_log(CreateLog(**message))
                print(f"Processed {message}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        consumer.close()


def save_log(log: CreateLog):
    with get_db() as session:
        session.add(db.Log(**log.model_dump()))


if __name__ == "__main__":
    consume()