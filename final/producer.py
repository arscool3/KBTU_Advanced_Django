import confluent_kafka

from schemas import KafkaRequest

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'contribution_requests_topic'


def produce(body: KafkaRequest) -> None:

    producer.produce(topic, body.model_dump_json())
    producer.flush()
