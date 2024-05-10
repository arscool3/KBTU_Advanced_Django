from datetime import datetime
import json
import time
import random
import confluent_kafka
from schemas import Heartbeat

producer = confluent_kafka.Producer({"bootstrap.servers": "localhost:9092"})
topic = "heartbeat_topic"

def generate_heartbeat_data():
    user_id = 1
    heart_rate = random.randint(60, 100)
    return Heartbeat(user_id=user_id, heart_rate=heart_rate)

def produce():
    try:
        while True:
            heartbeat_data = generate_heartbeat_data()
            print(f"Producing heartbeat data: {heartbeat_data}")
            producer.produce(topic=topic, value=json.dumps(heartbeat_data.dict()))
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()

if __name__ == "__main__":
    produce()
