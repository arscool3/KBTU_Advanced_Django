import dramatiq
import random

@dramatiq.actor
def validate(order_data):
    # Perform order calculations asynchronously
    validate = random.randint(0, 10) > 2
    print("Validating:", order_data, {"validate" : validate})