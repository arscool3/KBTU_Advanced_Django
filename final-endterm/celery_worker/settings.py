import os
import redis

__all__ = ['cache', 'CELERY_BROKER', 'DATABASE_URL']

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')
DATABASE_URL = os.environ.get("POSTGRES_URL", "postgresql://postgres:postgres@localhost/postgres")

cache = redis.Redis(host=REDIS_HOST, port=6379, db=1)
