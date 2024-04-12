import random
from typing import NewType
from schemas import Film
import confluent_kafka

Message = NewType('Message', str)

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "main_topic"


def produce(film: Film) -> None:
    producer.produce(topic=topic, value=film.model_dump_json())
    producer.flush()
    print(f"Produces message: {film} into {topic}")


if __name__ == "__main__":
    for i in range(100_000):
        message = Message(f"Hello, {i}!")
        produce(message)
