from fastapi import FastAPI

from producer import produce
from schemas import Restaurant

app = FastAPI()

@app.post('/restaurants')
def produce_restaurant(restaurant: Restaurant):
    produce(restaurant)
    return f'{restaurant.name} has been produced'
