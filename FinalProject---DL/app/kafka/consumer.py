# import confluent_kafka
# import json
#
# from app.database import session
# from app.models import Reservation
#
# from app.reservations.schemas import ReservationMessage
#
# consumer = confluent_kafka.Consumer(
#     {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
# )
# topic = "library_topic"
# consumer.subscribe([topic])
#
#
# def consume():
#     try:
#         while True:
#             messages = consumer.consume(num_messages=5, timeout=1.5)
#             for message in messages:
#                 reservation = ReservationMessage.model_validate(json.loads(message.value().decode("utf-8")))
#                 print(type(reservation))
#                 print(reservation)
#                 db = session()
#                 db.add(Reservation(**reservation.model_dump()))
#
#
#     except Exception as e:
#         print(f"Raised {e}")
#     finally:
#         consumer.close()
#
#
# if __name__ == '__main__':
#     consume()
