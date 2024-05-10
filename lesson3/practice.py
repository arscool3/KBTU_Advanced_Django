# CREATE 3 VIEWS WITH DEPENDECY INJECTION
# 2 WITH FUNCTION DEPENDENCY INJECTION
# 1 WITH INSTANCE OF CLASS AS CALLABLE DI


from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

laptops = []


class Laptop(BaseModel):
    model: str
    year: int


class LaptopSubLayer:
    def add_laptop(self, laptop: Laptop) -> str:
        laptops.append(laptop)
        return "Laptop was added"


class LaptopMainLayer:
    def __init__(self, repo:  LaptopSubLayer):
        self.repo = repo

    def __call__(self, laptop: Laptop) -> str:
        return self.repo.add_laptop(laptop)


laptop_sub_layer = LaptopSubLayer()
laptop_main_layer = LaptopMainLayer(repo=laptop_sub_layer)


def get_laptop_sub_layer_dependency() -> LaptopSubLayer:
    return laptop_sub_layer


def get_laptop_main_layer_dependency() -> LaptopMainLayer:
    return laptop_main_layer


@app.post('/laptops')
def add_laptop(laptop: Laptop, dep_func: callable = Depends(get_laptop_sub_layer_dependency)):
    return dep_func.add_laptop(laptop)


@app.post('/laptops-callable')
def add_laptop_callable(laptop: Laptop, dep_func: LaptopMainLayer = Depends(get_laptop_main_layer_dependency)):
    return dep_func(laptop)


@app.get('/laptops')
def get_laptops() -> list[Laptop]:
    return laptops
