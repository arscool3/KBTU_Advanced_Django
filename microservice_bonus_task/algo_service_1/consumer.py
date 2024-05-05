import datetime
import json
import confluent_kafka
from fastapi import Depends
from sqlalchemy.orm import Session
import models
from schemas import CreateData
from schemas import Binance
from database import session


consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)

topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 10


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


def consume(db: Session = Depends(get_db)):
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                binance = Binance.model_validate(json.loads(message.value().decode("utf-8")))
                data = CreateData(
                    time=datetime.datetime.now().__str__(),
                    name=f'{binance.pair.at_coin}_to_{binance.pair.from_coin}',
                    correlation_coefficient=11.16  # in here algo function
                )
                db.add(models.Data(**data.model_dump()))
                print("Data added to table!")
                print(f'data: {data.model_dump_json()}')
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()