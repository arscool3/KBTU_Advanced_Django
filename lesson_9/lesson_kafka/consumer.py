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
    distinct_partitions = set()
    index = 0
    try:
        while index <= 1000:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            if messages is None:
                continue
            print(distinct_partitions)
            index += len(messages)
            for message in messages:
                distinct_partitions.add(message.partition())
            if index > 1000:
                distinct_partitions.clear()
                index = 0
    except Exception as e:
        print(f'Raised {e}')
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()
