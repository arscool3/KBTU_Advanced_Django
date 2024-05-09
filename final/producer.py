import confluent_kafka
import json
import time


class KafkaProducer:
    def __init__(self, servers: str):
        self.producer = confluent_kafka.Producer(
            {"bootstrap.servers": servers}
        )

    def send_to_kafka(self, topic, entry):
        self.producer.produce(topic=topic, value=json.dumps(entry))
        self.producer.flush()

        print("producer is done")
        time.sleep(5)
