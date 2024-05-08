import confluent_kafka
import requests
import random
import time
from datetime import datetime

from schemas import CurrencyCreate

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)
topic = 'main_topic'


def get_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/KZT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        usd_to_kzt_rate = data['rates']['USD']
        eur_to_kzt_rate = data['rates']['EUR']
        return usd_to_kzt_rate, eur_to_kzt_rate
    else:
        print("Failed to fetch exchange rates")
        return None, None

def format_price(price):
    price_str = str(price)
    int_part, decimal_part = price_str.split('.')
    
    last_digit = str(random.randint(0, 9))
    random_integer = int_part[:-1] + last_digit
    
    random_decimal = ''.join(str(random.randint(0, 9)) for _ in range(len(decimal_part)))
    formatted_price = f'{random_integer}.{random_decimal}'
    
    return float(formatted_price)


def produce():
    cnt = 0
    while cnt < 20:
        usd_to_kzt_rate, eur_to_kzt_rate = get_exchange_rates()
        if usd_to_kzt_rate is not None and eur_to_kzt_rate is not None:
            usd_price_in_kzt = format_price(1 / usd_to_kzt_rate)
            eur_price_in_kzt = format_price(1 / eur_to_kzt_rate)

            current_time = datetime.now().isoformat()

            dollar_data = CurrencyCreate(
                time=current_time,
                price=usd_price_in_kzt,
                coin="usd" 
            )
            euro_data = CurrencyCreate(
                time=current_time,
                price=eur_price_in_kzt,
                coin="eur"
            )
            print(dollar_data.model_dump_json())
            print(euro_data.model_dump_json())
            producer.produce(topic=topic, value=dollar_data.model_dump_json())
            producer.produce(topic=topic, value=euro_data.model_dump_json())

        cnt += 1
        time.sleep(2)

if __name__ == '__main__':
    produce()
