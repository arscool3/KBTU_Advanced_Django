FROM python:3.11-slim as builder

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

FROM builder as runner

ENV HOST=0.0.0.0
ENV PORT=8000

COPY . /app

WORKDIR /app

CMD uvicorn main:api_app --host=${HOST} --port=${PORT} --reload

EXPOSE $PORT