import os
import pickle
import time
from datetime import datetime

# from dotenv import load_dotenv
import confluent_kafka
import httpx

import sys

sys.path.append("../../")
from database import WorkTime, session

sys.path.append("../../")

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
#
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     print("Error: .env file")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
binance_host = os.environ.get("INTERNAL_BINACE_HOST", "localhost:8002")
topic = os.environ.get("DEFAULT_TOPIC", "main_topic")
producer_host = os.environ.get("DEFAULT_PRODUCER_HOST", "127.0.0.1:8003")
timeout = int(os.environ.get("DEFAULT_TIMEOUT", 10))
producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def request_binance():
    time.sleep(1)  # to not DOS a server
    url = f"http://{binance_host}/currencies/"
    response = httpx.get(url)
    print(response.json())
    return response.json()


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


def request_main_server():
    time.sleep(5)  # to not DOS a server
    url = f"http://{producer_host}/healthcheck/"
    try:
        response = httpx.get(url, timeout=timeout)
        print(response.json())
        return True
    except:
        print("Death")


def start_processing():
    while True:
        if request_main_server():
            continue
        start_date = datetime.now()
        res = request_binance()
        produce(res)
        end_date = datetime.now()
        work_time_db = WorkTime(
            start_date=start_date,
            end_date=end_date
        )
        session.add(work_time_db)
        session.commit()


if __name__ == "__main__":
    start_processing()
