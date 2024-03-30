
import json
from database import SessionLocal
from models import FilmModel
import confluent_kafka

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9142", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20

def consume():
    session = SessionLocal()
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                if message.error():
                    print("Consumer error: {}".format(message.error()))
                    continue

                film_data = json.loads(message.value().decode("utf-8"))
                film = FilmModel(name=film_data['name'], director=film_data['director'])
                session.add(film)
                print(f"Added film: {film.name}, directed by {film.director}")
            session.commit()
    except Exception as e:
        print(f"Raised {e}")
    finally:
        session.close()
        consumer.close()

if __name__ == '__main__':
    consume()
