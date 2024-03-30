import json
import confluent_kafka

producer = confluent_kafka.Producer({"bootstrap.servers": "localhost:9092"})
topic = "main_topic"

def produce(film):
    producer.produce(topic, json.dumps(film))
    producer.flush()

if __name__ == "__main__":
    film = {"name": "Inception", "director": "Christopher Nolan"}
    produce(film)
