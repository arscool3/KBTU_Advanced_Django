from confluent_kafka import Producer
import json
import time
from datetime import datetime

class BitcoinProducer:
    def __init__(self, bootstrap_servers='localhost:9092', topic='binance_topic'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def produce_data(self):
        for _ in range(20):
            timestamp = datetime.now().isoformat()
            bitcoin1 = {
                "time": timestamp,
                "price": round(generate_price(100, 50), 2),
                "coin": "BTC"
            }
            bitcoin2 = {
                "time": timestamp,
                "price": round(generate_price(100, 40), 2),
                "coin": "ETH"
            }
            self.produce_message(bitcoin1)
            self.produce_message(bitcoin2)
            time.sleep(2)

    def produce_message(self, message):
        try:
            self.producer.produce(self.topic, json.dumps(message))
        except Exception as e:
            print(f"Failed to produce message: {e}")
        else:
            print(f"Message produced: {message}")

    def generate_price(self, base_price, max_offset):
        return base_price + time.time() % max_offset
    



if __name__ == '__main__':
    producer = BitcoinProducer()
    producer.produce_data()
