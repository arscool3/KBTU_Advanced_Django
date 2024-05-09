from database import Session
import redis
from confluent_kafka import Producer
import json
from schemas import OrderRead


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    try:
        yield redis_client
    finally:
        redis_client.close()


class KafkaManager:
    @staticmethod
    def get_producer():
        config = {'bootstrap.servers': 'localhost:9092'}
        return Producer(config)


def send_order_details(order_data):
    producer = KafkaManager.get_producer()
    order_data = OrderRead.from_orm(order_data).json()

    def delivery_report(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    producer.produce('order_topic', json.dumps(order_data).encode('utf-8'), callback=delivery_report)
    producer.flush()
