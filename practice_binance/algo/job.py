import time

import requests
import confluent_kafka
from algo.algo_layer import calculate_avg_price
from database import session
from schemas import Price


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 10


def check():
    while True:
        time.sleep(60)
        if requests.get('https://localhost/healthcheck') is False:
            start_processing()


def start_processing():
    while True:
        if requests.get('https://localhost/healthcheck'):
            break
        messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
        for message in messages:
            result = calculate_avg_price(message)
            new_price = Price(
                time=message['Open time'],
                name="Sample Name",
                price=result
            )
            session.add(new_price)
            try:
                session.commit()
            except Exception as e:
                print(f"Database error: {e}")
                session.rollback()
