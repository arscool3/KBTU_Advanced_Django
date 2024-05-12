import confluent_kafka
from schemas import Restaurant
from typing import NewType
# Message = NewType('Message', str)

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'main_topic'


def produce(restaurant: Restaurant):
    producer.produce(topic=topic, value=restaurant.model_dump_json())
    producer.flush()
    # print(f'Produced message {message} in topic {topic}')


if __name__ == '__main__':
    restaurants = [
        Restaurant(name='Tary', cuisine='Kazakh'),
        Restaurant(name='OTTB', cuisine='Kazakh fast food'),
        Restaurant(name='Mc Donals', cuisine='Fast Food'),
        Restaurant(name='Salam Bro', cuisine='Fast Food'),
        Restaurant(name='Del Papa', cuisine='Italian'),
        Restaurant(name='Papa Pizza', cuisine='Pizzeria'),
        Restaurant(name="Denny's", cuisine="America's Diner"),
    ]
    for restaurant in restaurants:
        produce(restaurant=restaurant)
