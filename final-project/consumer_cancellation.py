
import datetime
import confluent_kafka
import json
from background_tasks import notify_participants

consumer = confluent_kafka.Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ticket_system_event_cancellation',
    'auto.offset.reset': 'earliest'
})

topics = ['cancel']
consumer.subscribe(topics)


def consume():
    try:
        while True:
            messages = consumer.consume(timeout=2)
            if messages is None:
                continue
            if messages is not None:
                for message in messages:
                    try:
                        data = json.loads(message.value().decode('utf-8'))
                        print(f'At [{datetime.datetime.now()}] Message received: {data}')
                        notify_participants.send(data['user_id'], data['event_id'])
                    except json.JSONDecodeError:
                        print(f"Error decoding message: {message.value().decode('utf-8')}")
            consumer.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print("Consumer closed")


if __name__ == "__main__":
    consume()