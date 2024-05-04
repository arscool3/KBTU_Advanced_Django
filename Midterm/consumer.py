import json
from confluent_kafka import Consumer, KafkaError
from service import process_and_store_most_popular_product

def setup_consumer():
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'cart_item_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe(['cart_item_actions'])
    return consumer

def consume_messages(consumer):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Error: {msg.error()}")
                continue

            message = json.loads(msg.value().decode('utf-8'))
            print(f"Received message: {message}")
            action = message['action']
            if action == 'create':
                print(f"Product {message['product_id']} ('{message['product_name']}') added to cart.")
                most_popular = process_and_store_most_popular_product()
                print(f"Most popular product: {most_popular if most_popular else 'None'}")
            elif action == 'delete':
                print(f"Cart item {message['cart_item_id']} ('{message.get('product_name', 'N/A')}') deleted.")
    except KeyboardInterrupt:
        print("Stopping consumer.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consumer = setup_consumer()
    consume_messages(consumer)




# import json
# from confluent_kafka import Consumer, KafkaError
#
# from service import process_and_store_most_popular_product
#
#
# def setup_consumer():
#     consumer_config = {
#         'bootstrap.servers': 'localhost:9092',
#         'group.id': 'cart_item_group',
#         'auto.offset.reset': 'earliest',
#         'enable.auto.commit': True
#     }
#     consumer = Consumer(consumer_config)
#     consumer.subscribe(['cart_item_actions'])
#     return consumer
#
# def consume_messages(consumer):
#     try:
#         while True:
#             msg = consumer.poll(timeout=1.0)
#             if msg is None:
#                 continue
#             if msg.error():
#                 if msg.error().code() != KafkaError._PARTITION_EOF:
#                     print(f"Error: {msg.error()}")
#                 continue
#
#             message = json.loads(msg.value().decode('utf-8'))
#             print(f"Received message: {message}")
#             most_popular = process_and_store_most_popular_product()
#             action = message['action']
#             if action == 'create':
#                 print(f"Product {message['product_id']} ('{message['product_name']}') added to cart.")
#             elif action == 'delete':
#                 print(f"Cart item {message['cart_item_id']} ('{message.get('product_name', 'N/A')}') deleted.")
#             print(f"Most popular product: {most_popular}")
#     except KeyboardInterrupt:
#         print("Stopping consumer.")
#     finally:
#         consumer.close()
#
# if __name__ == "__main__":
#     consumer = setup_consumer()
#     consume_messages(consumer)
