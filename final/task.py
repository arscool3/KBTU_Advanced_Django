import dramatiq

@dramatiq.actor
def process_payment(payment_id):
    # Assuming you have a function to handle payment processing
    handle_payment_processing(payment_id)