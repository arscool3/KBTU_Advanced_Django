import json

import confluent_kafka
import websockets

from schemas import Binance, Currency, CurrencyPair
import asyncio

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'main_topic'

send_coin = Currency(cur_name="BTC", k="Bitcoin", amount=30.0)
get_coin = Currency(cur_name="ETH", k="Ethereum", amount=30.0)

currency_pair = CurrencyPair(send_coin=send_coin, get_coin=get_coin)


async def produce(binance: Binance):
    try:
        url = 'ws://localhost:8765'
        async with websockets.connect(url) as websocket:
            while True:
                await websocket.send(json.dumps(binance.model_dump()))
                print("Message sent")
                await asyncio.sleep(1)
                # producer.produce(topic=topic, value=binance.model_dump_json())
                # producer.flush()
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    binance_instance = Binance(
        start_date='2018-01-01',
        end_date='2022-02-02',
        interval='1d',
        pair=currency_pair
    )
    asyncio.run(produce(binance_instance))
