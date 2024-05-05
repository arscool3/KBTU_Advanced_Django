import os
import time
from dotenv import load_dotenv
from celery import Celery

load_dotenv(".env")

celery = Celery(__name__)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

# celery.conf.broker_url = "redis://127.0.0.1:6379/0"
# celery.conf.result_backend = "redis://127.0.0.1:6379/0"

@celery.task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c

