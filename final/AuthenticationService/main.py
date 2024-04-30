from fastapi import FastAPI

app = FastAPI()


@app.get("/health_check")
def health_check() -> dict:
    return {"message": "I'm alive"}
