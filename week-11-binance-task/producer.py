import confluent_kafka
from schemas import Bitcoin
import time
from datetime import datetime

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'binance_topic'


def produce():
    while True:
        bitcoin1 = Bitcoin(
            time=datetime.now().isoformat(),
            price=100 + time.time() % 50,
            coin="BTC"
        )
        bitcoin2 = Bitcoin(
            time=datetime.now().isoformat(),
            price=100 + time.time() % 40,
            coin="ETH"
        )
        print(bitcoin1.model_dump_json())
        print(bitcoin2.model_dump_json())
        producer.produce(topic=topic, value=bitcoin1.model_dump_json())
        producer.produce(topic=topic, value=bitcoin2.model_dump_json())
        producer.flush()
        time.sleep(5)


if __name__ == '__main__':
    produce()
