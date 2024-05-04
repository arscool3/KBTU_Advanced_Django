import json
import time

import confluent_kafka

from database import session
from schemas import BinanceDeal
from models import BinanceDealModel

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            messages_to_create = []
            for message in messages:
                binance_deal = BinanceDeal.model_validate(json.loads(message.value().decode("utf-8")))

                print(binance_deal)
                result = algo(binance_deal)

                messages_to_create.append(result)
            insert_db(messages_to_create)
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


def algo(binance_deal) -> BinanceDealModel:

    binance_deal_model = BinanceDealModel(
        symbol=binance_deal.pair,
        price=binance_deal.price,
        quantity=binance_deal.quantity,
        k_to_usd=calc_k_to_usd(binance_deal)
    )
    return binance_deal_model


def calc_k_to_usd(binance_deal):

    result = binance_deal.price / binance_deal.quantity
    rounded_result = round(result, 3)
    return rounded_result


def insert_db(binance_deals: list[BinanceDealModel]):
    db_session = session()
    for deals in binance_deals:

        db_session.add(deals)
    db_session.commit()
    print("Saved to DB!")


if __name__ == '__main__':
    consume()
