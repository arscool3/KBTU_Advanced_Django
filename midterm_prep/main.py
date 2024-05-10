from fastapi import FastAPI

app = FastAPI(title="Midterm Prep")

@app.get('/hello')
def hello():
    return "Hello World"