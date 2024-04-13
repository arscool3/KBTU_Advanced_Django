import confluent_kafka
from database import insert_to_db
from schemas import Bitcoin
import json

consumer = confluent_kafka.Consumer(
    {'bootstrap.servers': 'localhost:9092', 'group.id': 'binance_group'}
)

topic = 'binance_topic'
consumer.subscribe([topic])
number_of_messages = 30


def consume_data():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            if messages is None:
                continue
            for message in messages:
                bitcoin = Bitcoin.model_validate(json.loads(message.value().decode("utf-8")))
                print(bitcoin)
                insert_to_db(bitcoin)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print("Consumer closed")


if __name__ == '__main__':
    consume_data()
