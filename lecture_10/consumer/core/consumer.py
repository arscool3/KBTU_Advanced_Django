import os
import pickle
import confluent_kafka
import sys
sys.path.append("../../")
from database import Currency, session

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
GROUP_ID = os.environ.get("GROUP_ID", "main_group")
MESSAGE_NUM = os.environ.get("MESSAGE_NUM", 20)

consumer = confluent_kafka.Consumer({"bootstrap.servers": KAFKA_BOOTSTRAP, "group.id": GROUP_ID})

topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

consumer.subscribe([topic])


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=MESSAGE_NUM, timeout=0.1)
            for message in messages:
                data = pickle.loads(message.value())
                currencies = data["data"]
                timestamp = data["timestamp"]
                for currency in currencies:
                    print(f'{timestamp} - {currency}: {currencies.get(currency)} OK!')
                    currency_db = Currency(
                        name=str(currency),
                        timestamp=timestamp,
                        coefficient=currencies.get(currency)
                    )
                    session.add(currency_db)
            session.commit()

    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()