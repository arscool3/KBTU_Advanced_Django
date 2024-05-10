import json
import confluent_kafka
from schemas import Order

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "kafka:9092", "group.id": "main_group"}
)
topic1 = "restaurant_order_topic"
topic2 = 'customer_order_topic'
consumer.subscribe([topic2, topic1])
number_of_messages = 20


def consume():
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                order = Order.model_validate(json.loads(message.value().decode('utf-8')))
                if order.status == 'PAID':
                    print(order)
                elif order.status == 'READY':
                    print(order)
                else:
                    print(order)
    except Exception as e:
        print(f'Raised: {e}')
    finally:
        consumer.close()


if __name__ == '__main__':
    consume()
