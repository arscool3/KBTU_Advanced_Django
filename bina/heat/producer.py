import random
import json
from datetime import datetime, timedelta
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'main_topic'

def random_date(start, end):

    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def produce_data():
    start_period = datetime.strptime("20210101", "%Y%m%d")
    end_period = datetime.strptime("20211231", "%Y%m%d")

    while True:
        start_date = random_date(start_period, end_period)
        end_date = random_date(start_date, end_period)

        data = {
            'purchase_price': round(random.uniform(30000, 40000), 2),
            'sell_price': round(random.uniform(30000, 40000), 2),
            'start_date': start_date.strftime("%Y%m%d"),
            'end_date': end_date.strftime("%Y%m%d")
        }

        producer.produce(topic, value=json.dumps(data))
        producer.flush()
        print("done")

if __name__ == "__main__":
    produce_data()
