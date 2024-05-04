
import json

import confluent_kafka
import psycopg2

from schemas import Film

db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "December1225",
    "host": "localhost"
}

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20


def consume():
    connection = None
    try:
        connection = psycopg2.connect(**db_params)
        cur = connection.cursor()
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                film = Film.model_validate(json.loads(message.value().decode("utf-8")))
                cur.execute(
                    "INSERT INTO films (name, director) VALUES (%s, %s)",
                    (film.name, film.director)
                )
                connection.commit()
                print(type(film))
                print(film)
    except Exception as e:
        print(f"Raised {e}")
    finally:
        if connection is not None:
            connection.close()
        consumer.close()


if __name__ == '__main__':
    consume()
