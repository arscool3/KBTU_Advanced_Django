import confluent_kafka
from algo.algo_layer import calculate_avg_price
from database import session
from schemas import Price


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 2


health = True


def healthcheck():
    return health


def consume():
    global health
    try:
        while True:
            health = True
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                result = calculate_avg_price(message)
                new_price = Price(
                    time=message['Open time'],
                    name="Sample Name",
                    price=result
                )
                session.add(new_price)
                try:
                    session.commit()
                except Exception as e:
                    print(f"Database error: {e}")
                    session.rollback()

    except Exception as e:
        health = False
        print(f"Raised {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()