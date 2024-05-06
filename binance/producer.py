import confluent_kafka
import json
import time
from datetime import datetime


class BitcoinProducer:
    def __init__(self, bootstrap_servers='localhost:9092', topic='binance_topic'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = confluent_kafka.Producer({'bootstrap.servers': self.bootstrap_servers})

    def produce_data(self):
        counter = 0
        while counter < 20:
            bitcoin1 = {
                "time": datetime.now().isoformat(),
                "price": 100 + time.time() % 50,
                "coin": "BTC"
            }
            bitcoin2 = {
                "time": datetime.now().isoformat(),
                "price": 100 + time.time() % 40,
                "coin": "ETH"
            }
            self.produce_message(bitcoin1)
            self.produce_message(bitcoin2)
            counter += 1
            time.sleep(2)

    def produce_message(self, message):
        self.producer.produce(self.topic, value=json.dumps(message))
        self.producer.flush()


if __name__ == '__main__':
    producer = BitcoinProducer()
    producer.produce_data()
