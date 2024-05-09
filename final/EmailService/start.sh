#! /bin/bash

celery -A task:celery worker --loglevel=INFO & uvicorn main:app --reload --host 0.0.0.0 --port 8000