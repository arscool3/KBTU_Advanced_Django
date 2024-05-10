from fastapi import FastAPI, BackgroundTasks

from schemas import Info
from task import send_email_check
app = FastAPI()


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {'message': "I'm alive"}


@app.post("/send_message", tags=['test'])
def send_message(info: Info):
    send_email_check.delay(info.username, info.email, info.total, info.order_id, info.restaurant_id)
    return {'message': 'message send to email'}
