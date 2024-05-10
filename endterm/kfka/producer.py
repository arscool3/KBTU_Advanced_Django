from kafka import KafkaProducer
import json

class KafkaProducerWrapper:
    def __init__(self, servers):
        self.producer = KafkaProducer(bootstrap_servers=servers, value_serializer=lambda m: json.dumps(m).encode('utf-8'))

    def send_message(self, topic, message):
        """
        Отправляет сообщение в указанный топик Kafka.

        Args:
            topic (str): Название топика.
            message (dict): Сообщение в виде словаря.
        """
        self.producer.send(topic, message)
        self.producer.flush()

    def close(self):
        """
        Закрывает соединение с Kafka.
        """
        self.producer.close()
