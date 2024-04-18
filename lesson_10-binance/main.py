from fastapi import FastAPI
from producer import produce
from consumer import consume

app = FastAPI()

# produce()
consume()