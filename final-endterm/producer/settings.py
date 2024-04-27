import os

__all__ = ["KAFKA_BOOTSTRAP", "TOPIC"]

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.environ.get("DEFAULT_TOPIC", "traffic_data")
