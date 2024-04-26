from decouple import config
from dramatiq_kafka import KafkaBroker

kafka_broker = KafkaBroker(bootstrap_servers=config('KAFKA_URL'))

