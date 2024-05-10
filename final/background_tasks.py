import dramatiq
from random import randint
from fastapi import Depends
from dependencies import get_db
from database import Payment, PaymentType

@dramatiq.actor
def calculate_order(order_data):
    # Perform order calculations asynchronously
    print("Calculating order:", order_data)
    # Add your order calculation logic here

@dramatiq.actor
def validate_paymant(paymaent_data):
    # Perform order calculations asynchronously
    print("Validating:", paymaent_data)
    validate = (randint(0, 10) > 2)
    if validate:
        db = Depends(get_db)
        payment_updata = Payment(user_id=paymaent_data.user_id, amount=paymaent_data.amount, status="realized", payment_type=PaymentType[paymaent_data.payment_type])
        db.add(payment_updata)
        db.commit()
        db.refresh(payment_updata)
        print("success")
    else:
        print("unsuccess")
    # Add your order calculation logic here

