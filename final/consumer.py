import json
import confluent_kafka
from repositories import insert_heartbeat_to_db
from schemas import Heartbeat

consumer = confluent_kafka.Consumer({"bootstrap.servers": "localhost:9092", "group.id": "heartbeat_group"})
topic = "heartbeat_topic"
consumer.subscribe([topic])
number_of_messages = 20

def consume():
    try:
        message_count = 0
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=2)
            if messages is None:
                break
            for message in messages:
                heartbeat_data = Heartbeat(**json.loads(message.value().decode("utf-8")))
                print(f"Consumed heartbeat data: {heartbeat_data}")
                insert_heartbeat_to_db(heartbeat_data)
                message_count += 1
                if message_count >= number_of_messages:
                    print("All messages consumed")
                    continue
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Consumer closed")


if __name__ == "__main__":
    consume()
