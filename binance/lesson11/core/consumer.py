import json
from datetime import datetime

import confluent_kafka
from fastapi import Depends
from sqlalchemy.orm import Session

from lesson11 import database
from lesson11.core.schemas import CreateData, Binance
from lesson11.main import get_db

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 10


def health_check():
    return "I'm alive"


def consume(db: Session = Depends(get_db)):
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)

            if not messages:
                print("No messages")

            for message in messages:
                binance = Binance.model_validate(json.loads(message.value().decode("utf-8")))
                tradeData = CreateData(
                    time=datetime.now(),
                    name=f'{binance.pair.send_coin}_to_{binance.pair.get_coin}',
                    k_to_usd=binance.pair.send_coin.amount / binance.pair.get_coin.amount
                )
                db.add(database.Data(**tradeData.model_dump()))
                print("Data has been inserted")
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()
