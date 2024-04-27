import confluent_kafka
import json
import time
from services import fetch_binance_data

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "topic1"

symbols = ['BTCUSDT', 'ETHUSDT']
interval = '1h'
start_date = '2022-01-01 00:00:00'
end_date = '2022-01-02 00:00:00'


def produce(entry):
    producer.produce(topic=topic, value=entry)
    producer.flush()

    print("producer is done")
    time.sleep(5)


if __name__ == '__main__':
    produce()