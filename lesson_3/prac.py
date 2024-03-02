from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

cats = []
dogs = []
birds = []


class Animal(BaseModel):
    name: str
    kind: str


class Cat(Animal):
    pass


class Dog(Animal):
    pass


class Bird(Animal):
    pass


@app.post('/cat')
def add_cat(cat: Animal = Depends(Cat)) -> str:
    cats.append(cat)
    return "Cat was added"


@app.post('/dog')
def add_cat(dog: Animal = Depends(Dog)) -> str:
    dogs.append(dog)
    return "Dog was added"


@app.post('/bird')
def add_cat(bird: Animal = Depends(Bird)) -> str:
    birds.append(bird)
    return "Bird was added"


@app.get('/all')
def get_animals():
    return {"cats": cats}, {"dogs": dogs}, {"birds": birds}
