from celery import Celery
from celery import send_email
from fastapi import BackgroundTasks



app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def send_email(to, subject, body):
    pass

@app.task
def notify_staff(order_id):
    pass

@app.post("/make_purchase/")
async def make_purchase(background_tasks: BackgroundTasks, user_email: str, purchase_details: str):
    # Code to make purchase
    # Assuming you have some data like `user_email` and `purchase_details`
    
    # Add task to send confirmation email asynchronously
    background_tasks.add_task(send_email, user_email, purchase_details)

    return {"message": "Purchase made successfully. Confirmation email will be sent shortly."}
