from fastapi import FastAPI, HTTPException, Depends
from database.db import *
from repository import *
from typing import Type
import punq
from typing import List
from managerServices import receive_kafka_message
from kafka.consumer import kafka_consume
from confluent_kafka import KafkaError
from sqlalchemy.exc import SQLAlchemyError
import models.orderModel as _model
from schemas.orderSchema import Order

app = FastAPI()
session = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self) -> List[ReturnType]:
        return self.repo.get_all()


class Dependency1(Dependency):
    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: Type[AbcRepository]) -> punq.Container:
    db = SessionLocal()
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=db))
    container.register(Dependency)
    container.register(Dependency1)
    return container


app.add_api_route("/products", get_container(ProductRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/product_by_id", get_container(ProductRepository).resolve(Dependency1), methods=["GET"])


@app.post("/manager")
async def manager_process_orders():
    consumer = kafka_consume('topic1', 'group1')
    try:
        message = consumer.poll(timeout=1.0)
        if message is None:
            return {"message": "No messages received from Kafka."}
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                return {"message": "No more messages in Kafka queue."}
            else:
                raise HTTPException(status_code=500, detail=f"Kafka error: {message.error()}")
        receive_kafka_message(message.value().decode('utf-8'))
        return {"message": "Processed order from Kafka."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing orders: {e}")
    finally:
        consumer.close()


@app.get("/orders")
def get_orders(session: Session = Depends(get_db)):
    orders = session.execute(select(_model.Order)).scalars().all()
    return [Order.model_validate(order) for order in orders]
