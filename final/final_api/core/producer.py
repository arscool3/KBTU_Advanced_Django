# import json
# import time
# import uuid
#
# import confluent_kafka
#
# producer = confluent_kafka.Producer(
#     {"bootstrap.servers": "localhost:9092"}
# )
#
# topic = "message_topic"
#
# # TODO: move to another API
#
# def produce(message):
#     producer.produce(topic=topic, value=json.dumps(message).encode('utf-8'))
#     producer.flush()
#     print("Message sent to user")
#
#
# new_message = {
#     'sender_id': 1,
#     'chat_id': 1,
#     'content': 'Hello, how are you?'
# }
#
#
# if __name__ == "__main__":
#     while True:
#         produce(new_message)
#         time.sleep(1)
