import confluent_kafka
from schemas import BitcoinCreate
import time
from datetime import datetime
import random

producer = confluent_kafka.Producer({"bootstrap.servers": "localhost:9092"})
topic = 'binance_topic'

COINS = ["BTC", "ETH", "LTC", "XRP"]


def generate_random_price():
    return random.uniform(100, 200) 


def produce_bitcoin_data(coin, num_messages=20, interval=2):
    counter = 0
    while counter < num_messages:
        bitcoin = BitcoinCreate(
            time=datetime.now().isoformat(),
            price=generate_random_price(),
            coin=coin
        )
        print(bitcoin.model_dump_json())
        producer.produce(topic=topic, value=bitcoin.model_dump_json())
        counter += 1
        time.sleep(interval)


if __name__ == '__main__':
    for coin in COINS:
        produce_bitcoin_data(coin)
