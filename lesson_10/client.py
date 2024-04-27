import asyncio
import json
from producer import produce
import websockets
from websockets import ConnectionClosedOK


async def test_ws():
    url = 'ws://127.0.0.1:8000/data'
    try:
        async with websockets.connect(url) as websocket:
            while True:
                data = await websocket.recv()
                print(f"Received data : {json.loads(data)}")
                produce(json.loads(data))
    except ConnectionClosedOK as e:
        print('Connection was closed')


asyncio.run(test_ws())
