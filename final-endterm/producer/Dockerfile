FROM python:3.11-slim as builder

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

FROM builder as runner

COPY . /app

CMD ["python", "/app/main.py"]