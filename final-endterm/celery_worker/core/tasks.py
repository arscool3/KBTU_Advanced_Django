from celery_app import celery_app
from database import session, History, Person, Position, Location, Road, Region
from .schemas import TrafficData
from settings import cache

__all__ = ["calculate_traffic_task"]


@celery_app.task
def calculate_traffic_task(traffic_schema: dict):
    print("Calculating traffic...", traffic_schema)
    print("Calculating traffic...", TrafficData(**traffic_schema))




