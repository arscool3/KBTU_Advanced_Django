import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
import requests
from requests.exceptions import ReadTimeout

result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

def when_to_retry(number_of_retries: int, exc: Exception) -> bool:
    return isinstance(exc, ReadTimeout)


checks = [
    'drug',
    'psycho',
    'crime',
]


@dramatiq.actor(store_results=True)
def send_request_to_our_server(name: str) -> str:
    print("ok")
    for check in checks:
        response = requests.get(f"http://127.0.0.1:9000/{check}/?name={name}")
        is_ok = not response.json()
        if not is_ok:
            return "dangerous"
    return "ok"
#docker run -d --name redis -p 6379:6379 redis/redis-stack-server:latest