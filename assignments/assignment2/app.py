from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str


class Magazine(BaseModel):
    title: str
    year: int


db_magazine = []
db_book = []


class Dependency:
    def __init__(self, item_type: type[Book] | type[Magazine]):
        self.item_type = item_type

    def __call__(self):
        if self.item_type == Book:
            db_magazine.append()
        else:
            return Magazine
        return self.item_type


@app.get("/books")
def getItems() -> List[Book]:
    return db_book


@app.get("/magazines")
def getItems() -> List[Magazine]:
    return db_magazine


def test_di(item: Magazine | Book) -> str:
    db.append(item)
    return f"{type(item).__name__} added successfully"


@app.post("/book")
def postBook(di: str = Depends(test_di)) -> str:
    return di


@app.post("/magazine")
def postMagazine(di: str = Depends(test_di)) -> str:
    return di



class LiteratureSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_literature(self, literature: Book | Magazine):
        print(self.log_message)
        books.append(literature) if isinstance(literature, Book) else magazines.append(literature)


class LiteratureMainLayer:
    def __init__(self, repo: LiteratureSubLayer):
        self.repo = repo

    def add_literature(self, literature: Book | Magazine):
        print("SOME LOGGING")
        self.repo.add_literature(literature)
        print("END LOGGING")

        return "literature was added"

    def add_book(self, book: Book) -> str:
        return self.add_literature(book)

    def add_magazine(self, magazine: Magazine) -> str:
        return self.add_literature(magazine)

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(LiteratureSubLayer, instance=LiteratureSubLayer(log_message='I AM INSIDE SUB LAYER'))
    container.register(LiteratureMainLayer)
    return container


@app.post('/books')
def add_book(book: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_book)]) -> str:
    return book


@app.post('/magazines')
def add_magazine(magazine: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_book)]) -> str:
    return magazine
