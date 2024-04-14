FROM python

RUN pip install confluent_kafka httpx

COPY producer.py /producer/producer.py

WORKDIR /producer

CMD ["python", "producer.py"]