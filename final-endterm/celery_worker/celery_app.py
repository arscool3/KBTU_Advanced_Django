import os
from celery import Celery
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
# from kombu import Queue, Exchange
from pydantic import BaseModel
from datetime import datetime

import redis

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

cache = redis.Redis(host=REDIS_HOST, port=6379, db=0)

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

class Road(BaseModel):
    name: str
    region: int
    traffic_rate: float
    start_position: int
    end_position: int

    class Config:
        from_attributes = True


class Location(BaseModel):
    latitude: float
    longitude: float


class TrafficInnerData(BaseModel):
    timestamp: datetime
    location: Location
    speed: int
    acceleration: float
    direction: int


class TrafficData(BaseModel):
    person_id: int
    traffic_data: TrafficInnerData


@app.task
def perform(x, y):
    return x + y


@celery_app.post("/calculate/")
def calculate_traffic(traffic_data: TrafficData):
    # result = app.signature(
    #     "tasks.perform",
    #     queue="consumer",
    # ).delay(x, y)

    result = perform.delay()
    return JSONResponse({"task_id": result.id, "message": "OK"}, status_code=status.HTTP_201_CREATED)
