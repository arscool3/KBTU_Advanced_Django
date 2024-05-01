from confluent_kafka import Consumer
from database import insert_listened

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "worker",
    }
)

consumer.subscribe(['listened'])


def check_message(message):
    if message is None:
        return False
    if message.error():
        return False


BATCH_SIZE = 100
while True:
    batch = consumer.consume(num_messages=BATCH_SIZE, timeout=1.0)
    if batch is None:
        continue

    for message in batch:
        if not check_message(message):
            continue

        message_value = message.value()
        user_id = message_value.get('user_id')
        song_id = message_value.get('song_id')

        insert_listened(user_id, song_id)

    consumer.commit(asynchronous=False)

consumer.close()
