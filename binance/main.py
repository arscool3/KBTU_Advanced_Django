from fastapi import FastAPI, WebSocket
from typing import List
from kafka import KafkaConsumer

import json
import asyncio


app = FastAPI()

consumer = KafkaConsumer('binance_topic', bootstrap_servers=['localhost:9092'])



@app.websocket("/historical")
async def websocket_historical(websocket: WebSocket):
    await websocket.accept()
  

    consumer.subscribe(['binance_topic'])
    
    try:
        # Function to send data from Kafka to WebSocket client
        async def send_data():
            for message in consumer:
                bitcoin_data = json.loads(message.value)
                await websocket.send_text(json.dumps(bitcoin_data))

        # Run send_data function in a separate task
        await asyncio.create_task(send_data())
    finally:
        # Unsubscribe from Kafka topic upon WebSocket connection closure
        consumer.unsubscribe()
        consumer.close()

# WebSocket endpoint for live data retrieval
@app.websocket("/live")
async def websocket_live(websocket: WebSocket):
    await websocket.accept()
    
    # Subscribe to Kafka topic
    consumer.subscribe(['binance_topic'])
    
    try:
        # Function to send data from Kafka to WebSocket client
        async def send_data():
            for message in consumer:
                bitcoin_data = json.loads(message.value)
                await websocket.send_text(json.dumps(bitcoin_data))

        # Run send_data function in a separate task
        await asyncio.create_task(send_data())
    finally:
        # Unsubscribe from Kafka topic upon WebSocket connection closure
        consumer.unsubscribe()
        consumer.close()
