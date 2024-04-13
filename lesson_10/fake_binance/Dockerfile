FROM python as builder

RUN pip install fastapi uvicorn

COPY . /project

WORKDIR /project

CMD ["uvicorn", "binance_fake:binance_app", "--reload", "--host", "0.0.0.0", "--port", "8543"]

