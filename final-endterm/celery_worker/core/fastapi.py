from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .tasks import calculate_traffic_task
from .schemas import TrafficData

__all__ = ["celery_fastapi"]

celery_fastapi = FastAPI(title="Celery Worker", version="0.1.0")


@celery_fastapi.post("/calculate/")
async def calculate_traffic(traffic_data: TrafficData):
    result = calculate_traffic_task.delay(
        traffic_schema=traffic_data.dict()
    )
    return JSONResponse({"task_id": result.id, "message": "OK"}, status_code=status.HTTP_201_CREATED)
