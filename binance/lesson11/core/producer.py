# import confluent_kafka
# from schemas import Binance
#
# producer = confluent_kafka.Producer(
#     {"bootstrap.servers": "localhost:9092"}
# )
#
# topic = 'main_topic'
#
#
# def produce(binance: Binance) -> None:
#     try:
#         while True:
#             producer.produce(topic=topic, value=binance.model_dump_json())
#             producer.flush()
#             print("Message sent")
#     except Exception as e:
#         print(f"Exception: {e}")
#
#
# if __name__ == "__main__":
#     produce()
