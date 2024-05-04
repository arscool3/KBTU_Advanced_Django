import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results, ResultMissing
import requests
from requests.exceptions import ReadTimeout

from app.schemas import Director


result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

whitelist = [
    'Bakytzhan',
    'Merei',
    'Danial'
]


def check_director(director: Director):
    print(director.name)
    task = check_person_from_whitelist.send(director.name)
    return {'id': task.message_id}


def result(id: str):
    try:
        task = check_person_from_whitelist.message().copy(message_id=id)
        return result_backend.get_result(task)
    except ResultMissing:
        return "Waiting for all requests"


@dramatiq.actor(store_results=True)
def check_person_from_whitelist(name: str) -> str:
    for person_name in whitelist:
        if person_name == name:
            print(person_name, name)
            return "ok"
    return "dangerous"
