def process_payment(payment_id, amount):
    print(f"Processing payment with ID {payment_id} for ${amount}.")
    return {"status": "success", "payment_id": payment_id, "amount": amount}