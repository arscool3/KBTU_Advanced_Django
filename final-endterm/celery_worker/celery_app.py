import os
from celery import Celery
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
# from kombu import Queue, Exchange

CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')

app = Celery('tasks', broker=CELERY_BROKER)

celery_app = FastAPI(title="Celery Worker", version="0.1.0")

# default_exchange = Exchange("consumer", type="direct")
#
# consumer_queue = Queue('consumer', exchange=default_exchange, routing_key='consumer')

# app.conf.task_default_queue = consumer_queue
# app.conf.task_queues = (consumer_queue,)


# CELERY_IMPORTS = (
#     "tasks",
# )


@app.task
def perform(x, y):
    return x + y


@celery_app.post("/calculate/")
def calculate_traffic():
    x = 10
    y = 20

    # result = app.signature(
    #     "tasks.perform",
    #     queue="consumer",
    # ).delay(x, y)

    result = perform.delay(x, y)
    return JSONResponse({"task_id": result.id, "message": "OK"}, status_code=status.HTTP_201_CREATED)
