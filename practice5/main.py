from fastapi import FastAPI
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

films = [
    "Oppenheimer",
    "1+1",
    "Cars",
    "Barbie" 
]

@app.get('/films')
def get_films() -> list:
    return films

@app.post('/genre')
def add_genre() -> str:
    