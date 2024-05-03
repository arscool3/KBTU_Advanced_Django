import json

import confluent_kafka
from sqlalchemy.orm import Session

from algoservice.calculation import count_messages_per_user_chat
from database import Message
from database import session
from dramatiq_worker import notify_users_about_new_message
from repository.repository import MessageRepository

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "message_topic"
consumer.subscribe([topic])


def insert_message(session: Session, message_data: dict):
    db_message = Message(content=message_data["content"], sender_id=message_data["sender_id"],
                         chat_id=message_data["chat_id"])
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    print(f"Message added to database: {db_message}")
    messages = MessageRepository(session).get_all()
    message_counts = count_messages_per_user_chat(messages)
    print("Message counts per user chat:", message_counts)

    notify_users_about_new_message(message_data)


def consume(session: Session):
    try:
        while True:
            messages = consumer.consume(num_messages=1, timeout=1.5)
            if not messages:
                print("No messages")
                continue
            for message in messages:
                if message.error():
                    print(f"Error: {message.error()}")
                    continue
                message_data = json.loads(message.value().decode('utf-8'))   # decode message to json
                print(f"Received message from Kafka: {message_data}")
                insert_message(session, message_data)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    try:
        consume(session)
    finally:
        consumer.close()
