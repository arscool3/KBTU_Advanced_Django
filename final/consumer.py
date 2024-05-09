import confluent_kafka
import json
from main import topic
from services import send_notification

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "group_events", "auto.offset.reset": "earliest"}
)

consumer.subscribe([topic])


def get_kafka():
    try:
        while True:
            messages = consumer.consume()
            if messages is None:
                break
            for message in messages:
                event = json.loads(message.value().decode("utf-8"))
                if event['is_prohibited'] is True:
                    print("WARNING!!!")
                    # print(f"Prohibited action is detected in camera with ID {event['camera_id']}!")
                    send_notification(event=event)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print("consumer is closed")


if __name__ == '__main__':
    get_kafka()
