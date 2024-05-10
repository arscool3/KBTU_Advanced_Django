from fastapi import FastAPI
import uvicorn

app = FastAPI()

movie = [
    'gggg',
    'aaaaa',
    'ffffff',
    'hhhhhh'
]

@app.get('/movies')
def get_movies() -> list:
    return movie

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)