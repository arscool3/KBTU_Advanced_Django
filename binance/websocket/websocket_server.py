import asyncio
import websockets

clients = set()
server_address = 'localhost'
port = 8765

async def consumer_handler(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            print("Received message:", message)
        except websockets.exceptions.ConnectionClosedError:
            clients.remove(websocket)
            break

async def producer_handler(websocket, path):
    global clients
    clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            print("Received message from producer:", message)
            for client in clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosedError:
        clients.remove(websocket)

async def start_server():
    async with websockets.serve(producer_handler, server_address, port):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(start_server())
