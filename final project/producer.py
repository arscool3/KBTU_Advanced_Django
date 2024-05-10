import json
import confluent_kafka


producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"},
)

topic = "logs_topic"


def produce_log(data: dict):
    try:
        producer.produce(topic=topic, value=json.dumps(data))
        producer.flush()
        print(f"Data sent: {data}")
    except Exception as e:
        print(f"Exception: {e}. DATA: {data}")