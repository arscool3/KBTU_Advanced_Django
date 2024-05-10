from fastapi import FastAPI, BackgroundTasks
import uvicorn
from consumer import consume

app = FastAPI()


# 8001

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health_check")
def health_check() -> dict:
    return {"message": 'I am alive'}


if __name__ == "__main__":
    # background_task = BackgroundTasks()
    # background_task.add_task(consume)
    uvicorn.run(app, host="0.0.0.0", port=8001)
    # print('Hello,')
    # consume()
