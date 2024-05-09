import dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(redis_broker)

@dramatiq.actor
def send_email(email: str, message: str):
    print(f"Sending email to {email} with message: {message}")
