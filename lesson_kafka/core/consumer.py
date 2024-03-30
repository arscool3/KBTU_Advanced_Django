import confluent_kafka

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost: 9092", "group.id": "main_group"}
)

topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 20


def consume():
    try:
        values = set()
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            print("Consumed: ", len(messages))
            for m in messages:
                print(m.partition())
                print(m.value().decode("UTF-8"))
                values.add(m.value().decode("UTF-8"))

            print(len(values))
    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    consume()
