import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from background_task import process_payment

result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


@dramatiq.actor(store_results=True)
def async_process_payment(payment_id, amount):
    result = process_payment(payment_id, amount)
    print(f"Payment processed: {result}")