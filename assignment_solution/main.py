from punq import Container
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from typing import Annotated


app = FastAPI()


class AnimeItem(BaseModel):
    title: str
    year: int


anime_list = []


class AnimeRepository:
    def __init__(self):
        self.items = anime_list

    def add(self, anime: AnimeItem) -> AnimeItem:
        self.items.append(anime)
        return anime

    def get_anime_list(self) -> list[AnimeItem]:
        return self.items

    def __call__(self, *args, **kwargs) -> str:
        return AnimeRepository.__name__


def get_container() -> Container:
    container = Container()
    container.register(AnimeRepository)
    return container


@app.get("/anime")
def get_anime(anime: Annotated[str, Depends(get_container().resolve(AnimeRepository).get_anime_list)]) -> str:
    return anime


@app.post("/anime")
def create_anime(anime: Annotated[str, Depends(get_container().resolve(AnimeRepository).add)]) -> str:
    return anime


@app.get("/")
def get_app(new_app: Depends(AnimeRepository)) -> str:
    return new_app()
