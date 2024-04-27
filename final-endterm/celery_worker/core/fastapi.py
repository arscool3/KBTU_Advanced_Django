from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .tasks import perform
from .schemas import TrafficData

__all__ = ["celery_fastapi"]

celery_fastapi = FastAPI(title="Celery Worker", version="0.1.0")


@celery_fastapi.post("/calculate/")
def calculate_traffic(traffic_data: TrafficData):
    # result = app.signature(
    #     "tasks.perform",
    #     queue="consumer",
    # ).delay(x, y)

    result = perform.delay()
    return JSONResponse({"task_id": result.id, "message": "OK"}, status_code=status.HTTP_201_CREATED)
