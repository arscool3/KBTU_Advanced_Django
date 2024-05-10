from kafka import KafkaConsumer
import json
from dotenv import dotenv_values

config = dotenv_values('kafka.env')

consumer = KafkaConsumer(
    'Tasks',
    bootstrap_servers=[config.get('KAFKA_SERVER')],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(message)