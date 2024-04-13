import json
from datetime import datetime

import confluent_kafka
from fastapi import Depends
from sqlalchemy.orm import Session

from database import Data
from schemas import CreateData, Binance
from database import get_db

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
                send_coin_amount = binance.pair.send_coin.amount
                get_coin_amount = binance.pair.get_coin.amount

                if send_coin_amount is not None and get_coin_amount is not None and get_coin_amount != 0:
                    k_to_usd = send_coin_amount - get_coin_amount / get_coin_amount
                else:
                    k_to_usd = 0.0

                db = next(get_db())
                tradeData = CreateData(
                    time=datetime.now(),
                    name=f'{binance.pair.send_coin.cur_name}_to_{binance.pair.get_coin.cur_name}',
                    k_to_usd=k_to_usd
                )
                db.add(Data(**tradeData.model_dump()))
                print("Data has been inserted")
                db.commit()
    except Exception as e:
        print(f"Raised {e}")
    finally:
        db.close()
        # consumer.close()


if __name__ == '__main__':
    try:
        consume()
    finally:
        consumer.close()
