from http.client import HTTPException

from fastapi import FastAPI

from app.reservations.routers import router as user_router
from app.books.routers import router as account_router
from app.members.routers import router as transaction_router
from app.publishers.routers import router as category_router
from app.authors.routers import router as budget_router
from app.loans.routers import router as expense_router
from app.worker.celery_worker import add, check_book_availability, send_promotional_emails

app = FastAPI()

app.include_router(user_router)

app.include_router(account_router)

app.include_router(transaction_router)

app.include_router(category_router)

app.include_router(budget_router)

app.include_router(expense_router)


# @app.post("/reservation_message")
# def produce_reservation(res: Reservation):
#     produce_message(res)
#     return "Reservation produced"

# celery -A celery_worker.celery_app worker --loglevel=info

@app.get("/sample")
def get():
    return "hello world"


@app.get('/add/{x}/{y}')
def add_numbers(x: int, y: int):
    # Trigger the task in the background
    task = add.delay(x, y)
    return {"task_id": task.id, "status": "Processing"}


@app.get('/result/{task_id}')
def get_task_result(task_id: str):
    # Retrieve the task result
    result = add.AsyncResult(task_id)
    if result.state == 'PENDING':
        return {"task_id": task_id, "status": "Pending"}
    elif result.state == 'SUCCESS':
        return {"task_id": task_id, "status": "Success", "result": result.result}
    else:
        raise HTTPException(status_code=400, detail="Task not found or failed")


@app.post("/tasks/check_availability")
def trigger_check_availability():
    total = check_book_availability.delay()
    return {"message": f"Availability check task triggered {total}"}


@app.post("/tasks/send-promotions")
def trigger_send_promotional_emails():
    send_promotional_emails.delay()
    return {"message": "Promotional email task started"}
