from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .routers import router

__all__ = ["api_app"]

api_app = FastAPI(title="APIFastAPI")


def default_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        content={"message": str(exc)},
        status_code=exc.status_code,
    )


api_app.include_router(router)

api_app.add_exception_handler(status.HTTP_400_BAD_REQUEST, default_handler)
api_app.add_exception_handler(status.HTTP_403_FORBIDDEN, default_handler)
api_app.add_exception_handler(status.HTTP_404_NOT_FOUND, default_handler)
api_app.add_exception_handler(status.HTTP_408_REQUEST_TIMEOUT, default_handler)
api_app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, default_handler)
api_app.add_exception_handler(status.HTTP_504_GATEWAY_TIMEOUT, default_handler)
