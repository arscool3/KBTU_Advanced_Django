import time

from pydantic import BaseModel
from fastapi import FastAPI
from dramatiq.results.errors import ResultMissing

from dramatiq_job.main import factorial, send_request_to_our_server, result_backend

app = FastAPI()


class Employee(BaseModel):
    name: str
    age: int


@app.post("/add_employee")
def add_employee(employee: Employee):
    task = send_request_to_our_server.send(employee.name)
    return {'id': task.message_id}


@app.get("/result")
def result(id: str):
    try:
        task = send_request_to_our_server.message().copy(message_id=id)
        return result_backend.get_result(task)
    except ResultMissing:
        return "Waiting for all requests"