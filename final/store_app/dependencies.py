from database import Session
from schemas import OrderRead
from tasks import process_order

import json
import redis
import threading
from confluent_kafka import Producer, Consumer


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

    @staticmethod
    def get_consumer():
        config = {'bootstrap.servers': 'localhost:9092',
                  'group.id': 'order_group',
                  'auto.offset.reset': 'earliest'}
        return Consumer(config)


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


def take_order_details():
    consumer = KafkaManager.get_consumer()
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue

        order_data = json.dumps(msg.value().encode('utf-8'))
        process_order(order_data)


threading.Thread(target=take_order_details(), daemon=True).start()
