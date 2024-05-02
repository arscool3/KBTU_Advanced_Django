from celery_app import celery_app
from .calculate_traffic_function import calculate_traffic_function

__all__ = ["calculate_traffic_task"]


@celery_app.task(
    queue="calculations",
    name="calculate_traffic_task",
)
def calculate_traffic_task(traffic_schema: dict):
    calculate_traffic_function(traffic_schema=traffic_schema)
