import json

import confluent_kafka

from schemas import Film

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                film = Film.model_validate(json.loads(message.value().decode("utf-8")))
                print(type(film))
                print(film)
            # Create Postgres Table Message
            # Insert name and director



    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()