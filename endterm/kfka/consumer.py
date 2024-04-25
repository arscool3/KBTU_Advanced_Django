from kafka import KafkaConsumer
import json

class KafkaConsumerWrapper:
    def __init__(self, topic, servers, group_id):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def listen_messages(self, callback):
        """
        Прослушивает сообщения из Kafka и вызывает callback функцию для обработки каждого сообщения.

        Args:
            callback (function): Функция обратного вызова, которая принимает сообщение.
        """
        for message in self.consumer:
            callback(message.value)

    def close(self):
        """
        Закрывает соединение с Kafka.
        """
        self.consumer.close()
