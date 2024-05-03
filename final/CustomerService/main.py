from fastapi import FastAPI
from order import router

app = FastAPI()
app.include_router(router)


@app.get("/health_check", tags=['check'])
def health_check() -> dict:
    return {'message': "I'm alive"}
