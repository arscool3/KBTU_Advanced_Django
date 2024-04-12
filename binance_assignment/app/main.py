# from core.producer import produce
import time
from datetime import datetime
import random

from producer import produce
from schemas import BinanceDeal


def generate_trade():
    return BinanceDeal(pair="BTC-USD",
                       price=random.randrange(69000, 72000),
                       quantity=random.randrange(1, 100),
                       timestamp=datetime.utcnow().isoformat()
                       )


def main():
    while True:
        trade = generate_trade()
        produce(trade=trade)

        time.sleep(2)
        print(f"trade {trade} created!")


if __name__ == '__main__':
    main()
