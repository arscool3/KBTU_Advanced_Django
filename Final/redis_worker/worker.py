import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
import requests
import time
from requests.exceptions import ReadTimeout
from api.repositories.Repository import *
from redis_worker.tasks import *
import datetime

result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)



@dramatiq.actor(store_results=True)
def payment_operations(reservation_id: int, session: Session = Depends(get_db)):
    while True:
        response = requests.get(f"http://127.0.0.1:8000/{reservation_id}/order")
        details = response.json()
        pay_status = details.get("pay")
        if pay_status:
            update_order_status(reservation_id, session)
            return "Payment has been completed for reservation ID: {}".format(reservation_id)
        else:
            time.sleep(5)
    
    
@dramatiq.actor(store_results = True)
def analysis_of_order(order: mdl.Order, db: Session = Depends(get_db)):
    add_to_history(order, db)
    return{
        "total_revenue": total_orders_revenue_by_month(db),
        "average_order_price": average_order_price(db),
        "revenue_per_visitor":revenue_per_visitor(db), 
    }



    