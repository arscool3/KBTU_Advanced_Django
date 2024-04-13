import json
from fastapi import Depends
from sqlalchemy.orm.session import Session
import confluent_kafka
from database import session
from schemas import FilmBase, Film

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


def consume(session: Session = Depends(get_db)):
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                film = FilmBase.model_validate(json.loads(message.value().decode("utf-8")))
                print(type(film))
                print(film)
                session.add(Film(**film.model_dump()))
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()