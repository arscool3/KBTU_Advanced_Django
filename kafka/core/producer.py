from schemas import Film
import confluent_kafka
import random

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "main_topic"

def produce(film: Film ) -> None:
    producer.produce(topic=topic, value=film.model_dump_json())
    producer.flush()

if __name__ == '__main__':

    for i in range(100_000):
        films = [
            Film(
                name='Alex',
                director='Marmelad',
            ),
            Film(
                name="Interstellar",
                director='Nolan'
            ),
            Film(
                name='1+1',
                director='idk'
            ),
            Film(
                name="rust",
                director='muller'
            ),
            Film(
                name='Yes',
                director='no'
            )
        ]
        if i % 1_000 == 0:
            print(f'produced {i} events')
        produce(random.choice(films))