from confluent_kafka import Consumer, KafkaError


def kafka_consume(topic_name, group_id, bootstrap_servers='localhost:9092'):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic_name])
    return consumer