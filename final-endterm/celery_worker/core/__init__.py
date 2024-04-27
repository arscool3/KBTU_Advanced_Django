from .fastapi import celery_fastapi
from .tasks import calculate_traffic_task

__all__ = ['celery_fastapi', "calculate_traffic_task"]
