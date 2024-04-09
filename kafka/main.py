from confluent_kafka import Producer
from fastapi import FastAPI

import models
import utils
import database

app = FastAPI()

producer_config = {
    'bootstrap.servers': 'kafka:9092'
}
producer = Producer(**producer_config)

db = database.client.chat_db
messages_collection = db.messages


@app.post("/send_message/")
def send_message(message: models.Message):
    producer.produce('chat_topic', message.message.encode('utf-8'), callback=utils.acked)
    producer.poll(0)

    messages_collection.insert_one({"message": message.message})

    return {"message": "Message sent successfully"}
