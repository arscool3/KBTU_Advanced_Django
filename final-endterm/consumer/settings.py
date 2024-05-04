import os

__all__ = ["KAFKA_BOOTSTRAP", "GROUP_ID", "MESSAGE_NUM", "TOPIC", "CELERY_SERVER"]

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
GROUP_ID = os.environ.get("GROUP_ID", "main_group")
MESSAGE_NUM = os.environ.get("MESSAGE_NUM", 1)
TOPIC = os.environ.get("DEFAULT_TOPIC", "traffic_data")
CELERY_SERVER = os.environ.get("CELERY_SERVER", "http://localhost:8888")
broker_url = os.environ.get("CELERY_BROKER", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
