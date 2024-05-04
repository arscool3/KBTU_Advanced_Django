import os
import time
from dotenv import load_dotenv
from celery import Celery
import app.models as db
from database import session
from sqlalchemy import func
from fastapi import BackgroundTasks

load_dotenv(".env")

celery = Celery(__name__)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

@celery.task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c

