# import json
#
# import confluent_kafka
#
# from app.models import Reservation
#
# producer = confluent_kafka.Producer(
#     {"bootstrap.servers": "localhost:9092"}
# )
#
# topic = "library_topic"
#
#
# def produce_message(data: Reservation):
#     try:
#         producer.produce(topic=topic, value=json.dumps(data))
#         producer.flush()
#         print(f"Sent message: {data}")
#     except Exception as e:
#         print(f"Exception: {e}. DATA: {data}")