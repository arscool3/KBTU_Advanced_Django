import os
import redis
from celery import Celery

__all__ = ['celery_app', 'cache']

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')
DATABASE_URL = os.environ.get("POSTGRES_URL", "postgresql://postgres:postgres@localhost/postgres")

celery_app = Celery('tasks', broker=CELERY_BROKER)

cache = redis.Redis(host=REDIS_HOST, port=6379, db=1)
