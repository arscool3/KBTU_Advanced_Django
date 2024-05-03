from fastapi import FastAPI
from pydantic import BaseModel

from producer import produce
from schemas import Message

app = FastAPI()


class NewMessage(BaseModel):
    sender_id: int
    chat_id: int
    content: str


@app.get("/")
def root():
    return "OK"


@app.post("/message")
def send_message(message: NewMessage):
    produce(message.dict())
    return "Message sent successfully"
