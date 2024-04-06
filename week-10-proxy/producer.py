import confluent_kafka
from schemas import Restaurant

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'main_topic'

def produce(restaurant: Restaurant):
    producer.produce(topic=topic, value=restaurant.model_dump_json())
    producer.flush()

