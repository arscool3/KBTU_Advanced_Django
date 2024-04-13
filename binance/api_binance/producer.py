import confluent_kafka
from schemas import Binance, Currency, CurrencyPair

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'main_topic'

send_coin = Currency(cur_name="BTC", k="Bitcoin", amount=30.0)
get_coin = Currency(cur_name="ETH", k="Ethereum", amount=30.0)

currency_pair = CurrencyPair(send_coin=send_coin, get_coin=get_coin)


def produce(binance: Binance):
    try:
        while True:
            producer.produce(topic=topic, value=binance.model_dump_json())
            producer.flush()
            print("Message sent")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    binance_instance = Binance(
        start_date='2018-01-01',
        end_date='2022-02-02',
        interval='1d',
        pair=currency_pair
    )
    produce(binance_instance)
