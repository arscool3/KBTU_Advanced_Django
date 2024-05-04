import dramatiq

broker = dramatiq.get_broker()

@dramatiq.actor
def send_email(email: str, message: str):
    print(f"Sending email to {email} with message: {message}")
