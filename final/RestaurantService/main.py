from fastapi import FastAPI

app = FastAPI()


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {'message': "I'm alive"}
