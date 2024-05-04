import asyncio
from confluent_kafka import Producer


producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'main_topic'

def produce_inventory_update(topic, product_id, quantity):
    message = f"{product_id}:{quantity}".encode('utf-8')
    producer.send(topic, value=message)
    producer.flush()
    producer.close()

