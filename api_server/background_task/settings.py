import time

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import CurrentMessageMiddleware


broker = RedisBroker(url="redis://localhost:6379/0")
dramatiq.set_broker(broker)
dramatiq.middleware_stack.push(CurrentMessageMiddleware())

@dramatiq.actor()
def spotify_wrapped_background_task():
    time.sleep(1000)
    return 'spotify_wrapped_background_task_completed'


