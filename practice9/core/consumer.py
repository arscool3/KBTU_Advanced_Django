import confluent_kafka
from producer import topic
import pickle

from database import session
from schemas import HeatMap
consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092",  "group.id": "main_group"}

)

consumer.subscribe([topic])

number_of_message = 20

def consume(): 
    try:
        while True:
            messages = consumer.consume(num_messages=number_of_message, timeout=1.5)
            for message in messages:
                data = pickle.loads(message.value())
                session.add(HeatMap(time = data.get("time"), 
                                    data = data.get("data") ))
            session.commit()
    except Exception as e:
        print("Raised", e)
    finally:
        consumer.close()

if __name__ == '__main__':
    consume()


