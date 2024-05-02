import os
import redis

__all__ = ['cache', 'broker_url', 'DATABASE_URL', "result_backend"]

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
DATABASE_URL = os.environ.get("POSTGRES_URL", "postgresql://postgres:postgres@localhost/postgres")

cache = redis.Redis(host=REDIS_HOST, port=6379, db=1)

broker_url = os.environ.get("CELERY_BROKER", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
