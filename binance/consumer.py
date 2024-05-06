import confluent_kafka
import schemas
from reposiroty import insert_to_db
import json

consumer = confluent_kafka.Consumer(
    {'bootstrap.servers': 'localhost:9092', 'group.id': 'binance_group'}
)

topic = 'binance_topic'
consumer.subscribe([topic])
number_of_messages = 30


def consume():
    try:
        message_count = 0
        while message_count < 20:  # Limit the number of messages consumed
            messages = consumer.consume(num_messages=number_of_messages, timeout=2)
            if not messages:
                break
            for message in messages:
                try:
                    bitcoin = schemas.BitcoinCreate(**json.loads(message.value().decode("utf-8")))
                    print(bitcoin)
                    insert_to_db(bitcoin)
                    message_count += 1
                except Exception as e:
                    print(f"Error processing message: {e}")
        print("All messages consumed")
    except KeyboardInterrupt:
        print("Consumer interrupted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print("Consumer closed")


if __name__ == '__main__':
    consume()