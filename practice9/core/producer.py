from confluent_kafka import Producer
import httpx, pickle


producer = Producer(
    {"bootstrap.servers": "localhost: 9092"}
)

topic = "binance_topic"


def get_binance_data(symbol: str):
    url = f"http://127.0.0.1:8999/data/{symbol}"
    return httpx.get(url).json()

def produce(request: dict):
    producer.produce(topic = topic, value =pickle.dumps(request))


if __name__ == "__main__":
    symbols = ["USDT/TNG", "BTC/ETH", "EUR/RUB", "RUB/TNG", "EUR/TNG"]
    for i in range(20):
        produce(get_binance_data(symbols[i%5]))