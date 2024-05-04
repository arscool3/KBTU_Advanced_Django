import os

__all__ = ["KAFKA_BOOTSTRAP", "TOPIC", "SLEEP_TIME"]

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.environ.get("DEFAULT_TOPIC", "traffic_data")
SLEEP_TIME = float(os.environ.get("SLEEP_TIME", 1))
