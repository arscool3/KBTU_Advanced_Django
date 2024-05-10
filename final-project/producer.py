from confluent_kafka import Producer
import json
import models
import schemas
import random
import time
from database import session

producer_config = {
    'bootstrap.servers': "localhost:9092"
}
producer = Producer(producer_config)


def produce_purchase(request: schemas.PurchaseRequest):
    message = {
        'user_id': request.user_id,
        'event_id': request.event_id,
    }
    producer.produce('purchase', value=json.dumps(message).encode('utf-8'))
    producer.flush()


def produce_cancellation(event_id):
    db_participants = session.query(models.Ticket).filter(models.Ticket.event_id == event_id)

    for db_participant in db_participants:
        participant = schemas.Ticket.model_validate(db_participant)
        db_user = session.query(models.User).filter(models.User.id == participant.user_id).first()
        user = schemas.User.model_validate(db_user)
        message = {
            "subject": "Event Cancelled",
            "user_id": user.id,
            "event_id": event_id
        }
        producer.produce('cancel', value=json.dumps(message).encode('utf-8'))
    producer.flush()


def produce_large_number_of_purchases(num_messages):
    user_count = session.query(models.User).count()
    event_count = session.query(models.Event).count()
    counter = 0

    while counter < num_messages:
        user_id = random.randint(1, user_count)
        event_id = random.randint(1, event_count)
        message = {
            'user_id': user_id,
            'event_id': event_id
        }
        counter += 1
        time.sleep(2)
        producer.produce('purchase', value=json.dumps(message).encode('utf-8'))
        producer.flush()
