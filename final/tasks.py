import dramatiq
from database import Appointment, session
import datetime

from dramatiq.brokers.redis import RedisBroker
import datetime 
redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def delete_all_appointments(data):
    while True:
        db = session 
        try:
            appointments = db.query(Appointment).all()
            
            for appointment in appointments:
                current_month = datetime.datetime.now().month
                if(current_month > appointment.month):
                    db.delete(appointment)
            # db.query(Appointment).filter(
            #     Appointment.appointment_datetime.month == 4
            # ).delete()
            db.commit()
        finally:
            db.close() 

delete_all_appointments.send("Delete appointments with month value 4")
