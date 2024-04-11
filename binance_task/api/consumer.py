import json

import confluent_kafka

from database import session
from models import CryptoTrade
from schemas import Message, CreateCryptoTrade
from services.algo import process_binance_msg

consumer = confluent_kafka.Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "main_group",
    }
)

topic = "binance_topic"

consumer.subscribe([topic])


def _insert_db(res: CreateCryptoTrade):
    db_session = session()
    db_session.add(CryptoTrade(**res.model_dump()))
    db_session.commit()


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=5, timeout=1.5)
            if not messages:
                print("no messages")
            for message in messages:
                message = json.loads(message.value().decode("utf-8"))
                res = process_binance_msg(Message(**message))
                _insert_db(res)
                print(f"Inserted {message}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()
