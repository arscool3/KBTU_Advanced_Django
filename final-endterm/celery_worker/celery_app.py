from celery import Celery
from settings import CELERY_BROKER

celery_app = Celery('tasks', broker=CELERY_BROKER)
