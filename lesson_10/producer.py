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


def produce():
    for symbol in symbols:
        data = fetch_binance_data(symbol, interval, start_date, end_date)
        for entry in data:
            producer.produce(topic=topic, value=json.dumps(entry))
            producer.flush()
            # print(entry)
            print("producer is done")
        time.sleep(10)


if __name__ == '__main__':
    produce()