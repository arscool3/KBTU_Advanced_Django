import json
import confluent_kafka

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "topic1"


async def send_to_kafka(products):
    order_data = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    producer.produce(topic=topic, value=json.dumps(order_data))
    producer.flush()
    print("producer is done")
