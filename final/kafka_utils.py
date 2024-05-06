from kafka import KafkaProducer, KafkaConsumer

def create_kafka_producer():
    return KafkaProducer(bootstrap_servers=['localhost:9092'])

def create_kafka_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='my-group')

if __name__ == "__main__":
    producer = create_kafka_producer()
    consumer = create_kafka_consumer('my-topic')
