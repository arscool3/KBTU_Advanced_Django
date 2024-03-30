from fastapi import FastAPI

from schemas import Film
from producer import produce

app = FastAPI()



@app.post("/film")
def produce_film(film: Film):
    produce(film)
    return "You film has processed"
