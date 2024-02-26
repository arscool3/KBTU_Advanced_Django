from __future__ import annotations

from typing import Annotated

import punq
from pydantic import BaseModel
from fastapi import FastAPI, Depends

app = FastAPI()


class Magazine(BaseModel):
    title: str
    content: str
    desc: str


class Fashion(Magazine):
    pass


class Sport(Magazine):
    pass


class Business(Magazine):
    pass


fashions = []
sports = []
business = []


class MagazineSubLayer:

    def __init__(self, log_message: str):
        self.log_message = log_message

    async def __call__(self):
        # return {"message": self.log_message, "name": "Golovkin"}
        return sports

    def add_magazine(self, magazine: Fashion | Sport | Business):

        print(self.log_message)

        if isinstance(magazine, Fashion):
            fashions.append(magazine)

        elif isinstance(magazine, Sport):
            sports.append(magazine)

        else:
            business.append(magazine)


class MagazineMainLayer:
    def __init__(self, repo: MagazineSubLayer):
        self.repo = repo

    def add_magazine(self, magazine: Fashion | Sport | Business) -> str:
        self.repo.add_magazine(magazine)
        return "Data was added"

    def add_fashion(self, fashion: Fashion) -> str:
        return self.add_magazine(fashion)

    def add_sport(self, sport: Sport):
        return self.add_magazine(sport)

    def add_business(self, firm: Business):
        return self.add_magazine(firm)


def get_container() -> punq.Container:
    container = punq.Container()
    container.register(
        MagazineSubLayer,
        instance=MagazineSubLayer(log_message="Inside SUB LAYER")
    )
    container.register(MagazineMainLayer)
    return container


@app.get("/fashions")
async def get_fashions() -> list[Fashion]:
    return fashions


@app.get("/sports")
async def get_sports() -> list[Sport]:
    return sports


@app.get("/business")
async def get_business() -> list[Business]:
    return business


@app.post("/fashions/add_fashion")
def add_fashion(fashion: Annotated[str, Depends(get_container().resolve(MagazineMainLayer).add_fashion)]) -> str:
    return fashion


@app.post("/sports/add_sport")
def add_sport(sport: Annotated[str, Depends(get_container().resolve(MagazineMainLayer).add_sport)]) -> str:
    return sport


@app.post("/business/add_business")
def add_business(firm: Annotated[str, Depends(get_container().resolve(MagazineMainLayer).add_business)]) -> str:
    return firm


magazineSubLayer = MagazineSubLayer("Callable DI with SUB LAYER")


@app.get("/sports/v1")
async def get_sports_v1(sport: list[Sport] = Depends(magazineSubLayer)):
    return sport
