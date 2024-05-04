import dramatiq
from dramatiq.brokers.redis import RedisBroker

# Setup Dramatiq with Redis
redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)
