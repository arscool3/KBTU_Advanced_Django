FROM python:3.12-slim as builder

COPY requirements.txt /needed/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /needed/requirements.txt


FROM builder as runner

ARG HOST=localhost
ARG PORT=8000

COPY . /celery

WORKDIR /celery

CMD uvicorn main:celery_fastapi --host=${HOST} --port=${PORT} --reload

EXPOSE $PORT
