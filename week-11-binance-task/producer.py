import confluent_kafka
from schemas import Bitcoin, BitcoinCreate
import time
from datetime import datetime

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'binance_topic'


def produce():
    counter = 0
    while counter < 20:
        bitcoin1 = BitcoinCreate(
            time=datetime.now().isoformat(),
            price=100 + time.time() % 50,
            coin="BTC"
        )
        bitcoin2 = BitcoinCreate(
            time=datetime.now().isoformat(),
            price=100 + time.time() % 40,
            coin="ETH"
        )
        print(bitcoin1.model_dump_json())
        print(bitcoin2.model_dump_json())
        producer.produce(topic=topic, value=bitcoin1.model_dump_json())
        producer.produce(topic=topic, value=bitcoin2.model_dump_json())
        counter += 1
        time.sleep(2)


if __name__ == '__main__':
    produce()
