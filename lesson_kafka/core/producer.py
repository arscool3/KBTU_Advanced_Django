from typing import NewType

import confluent_kafka

Message = NewType("Message", str)

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost: 9092"}
)

topic = "main_topic"


def produce(message: Message) -> None:
    producer.produce(topic=topic, value=message)
    producer.flush()


if __name__ == "__main__":
    for i in range(100_000):
        message = Message(f"Hello, {i}!")
        # if i % 1_000 == 0:
            # print("produced", i)
        produce(message)
