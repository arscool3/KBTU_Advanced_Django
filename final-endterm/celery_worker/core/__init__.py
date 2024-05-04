# from .fastapi import celery_fastapi
from .tasks import calculate_traffic_task

__all__ = ["calculate_traffic_task"]
