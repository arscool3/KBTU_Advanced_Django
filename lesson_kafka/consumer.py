import json

import confluent_kafka

import models
from database import session
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
            films = []
            for message in messages:
                film = Film.model_validate(json.loads(message.value().decode("utf-8")))
                print(type(film))
                print(film)
                films.append(film)
            insert_film(films)
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


def insert_film(films: list[Film]):
    db_session = session()
    films_to_insert = [models.Film(**film.model_dump()) for film in films]
    db_session.bulk_save_objects(films_to_insert)
    db_session.commit()


if __name__ == '__main__':
    consume()
