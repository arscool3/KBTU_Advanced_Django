import confluent_kafka
import api.models.models as mdl

from redis_worker.worker import analysis_of_order, result_backend
from api.repositories.Repository import *

import json

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost: 9092", "group.id": "main_group"}
)

topic = "order-events"
consumer.subscribe([topic])
number_of_messages = 5

def consume(db: Session = Depends(get_db)):
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                order = mdl.Order.model_validate(json.loads(message.value().decode("utf-8")))
                analysis_of_order.send(order, db)
                print(type(message))
                print(message.value().decode("utf-8"))
    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()
