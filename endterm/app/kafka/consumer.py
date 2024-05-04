import json

import confluent_kafka

from app.database import session
from app.models import AccessLogJournal
from app.schemas import JournalMessage

consumer = confluent_kafka.Consumer(
    {
        "bootstrap.servers": f"localhost:9092",
        "group.id": "main_group",
    }
)

topic = "journal_logs_topic"

consumer.subscribe([topic])


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=5, timeout=1.5)
            if not messages:
                print("no messages")
            for message in messages:
                print(f"Incoming message: {message.value()}")
                message = json.loads(message.value().decode("utf-8"))
                _process_access_logs_message(JournalMessage(**message))
                print(f"Processed {message}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        consumer.close()


def _process_access_logs_message(message: JournalMessage):
    db_session = session()

    db_session.add(AccessLogJournal(**message.model_dump()))
    db_session.commit()


if __name__ == "__main__":
    consume()
