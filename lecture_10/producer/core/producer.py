import os
import pickle
import time
from dotenv import load_dotenv
import confluent_kafka
import httpx

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Error: .env file")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
binance_host = os.environ.get("INTERNAL_BINACE_HOST", "localhost:8022")
topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def request_binance():
    time.sleep(2)  # to not DOS a server
    url = f"http://{binance_host}/currencies/"
    response = httpx.get(url)
    print(response.json())
    return response.json()


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


if __name__ == "__main__":
    while True:
        res = request_binance()
        produce(res)