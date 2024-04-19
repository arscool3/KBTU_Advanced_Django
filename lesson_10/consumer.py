import confluent_kafka
from services import insert_data_to_db
from schemas import BitcoinCreate
import json

consumer = confluent_kafka.Consumer(
    {'bootstrap.servers': 'localhost:9092', 'group.id': 'group6'}
)

topic = 'topic6'
consumer.subscribe([topic])
number_of_messages = 30


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1)
            if messages is None:
                continue
            for message in messages:
                print(message.value().decode("utf-8"))
                bitcoin = BitcoinCreate(**json.loads(message.value().decode("utf-8")))
                print(bitcoin)
                insert_data_to_db(bitcoin)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()

