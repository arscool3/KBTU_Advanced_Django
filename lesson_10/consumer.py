import confluent_kafka
from services import insert_data_to_db
from schemas import BaseBitcoin
import json
from producer import topic

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "group_binance", "auto.offset.reset": "earliest"}
)

consumer.subscribe([topic])
number_of_messages = 30


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=2)
            if messages is None:
                break
            for message in messages:
                print("----")
                print(json.loads(message.value().decode("utf-8")))
                print("----")
                bitcoin_data = json.loads(message.value().decode("utf-8"))
                bitcoin_create = BaseBitcoin(**bitcoin_data)
                # print(bitcoin_create)
                insert_data_to_db(bitcoin_create)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print("consumer is closed")


if __name__ == '__main__':
    consume()