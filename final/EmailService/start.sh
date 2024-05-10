#! /bin/bash

celery -A task:celery worker --loglevel=INFO & \
celery -A task:celery flower & \ 
uvicorn main:app --reload --host 0.0.0.0 --port 8000