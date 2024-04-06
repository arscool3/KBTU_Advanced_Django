import confluent_kafka
consumer = confluent_kafka.Consumer(
    {'bootstrap.servers': 'localhost:9092', 'group.id': 'main_group'}
)

topic = 'main_topic'
consumer.subscribe([topic])
number_of_messages = 30


def consume():
    distinct_partitions = set()
    index = 0
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            if messages is None:
                continue
            # print(f'Consumed {len(messages)}')
            print(distinct_partitions)
            index += len(messages)
            if index > 1000:
                distinct_partitions.clear()
                index = 0
            for message in messages:
                distinct_partitions.add(message.partition())
                # print(f"""
                # {message.partition()}
                # {message.value().decode('utf-8')}
                # """)
    except Exception as e:
        print(f'Raised {e}')
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()
