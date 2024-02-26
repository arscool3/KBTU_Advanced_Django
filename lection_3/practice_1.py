from fastapi import Depends, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Literature(BaseModel):
    title: str
    author: str


class Book(Literature):
    extra: int


class Magazine(Literature):
    pass


literatures = []

return_test = tuple[str, list]


def get_from_db_by_title(title: str = Path()) -> Book:
    books = list(filter(lambda x: x.title == title, literatures))
    return books[0]


class CreateDependency:
    def __init__(self, literature_type: type[Book] | type[Magazine]):
        self.literature_type = literature_type

    def __call__(self, literature: Literature):
        if self.literature_type == Book:
            literatures.append(literature)
        else:
            literatures.append(literature)

        return "{} was added".format(self.literature_type)


def dep_factory(lit_type):
    def add_literature_dep(literature: lit_type):
        literatures.append(literature)
        return "{} was added".format(type(literature))

    return add_literature_dep


@app.get("/all/")
def get_all():
    return literatures


@app.post("/book/")
def add_book(res: str = Depends(dep_factory(Book))):
    return res


@app.post("/magazine/")
def add_magazine(res: str = Depends(CreateDependency(Magazine))):
    return res


@app.get("/books/{title}")
def get_book_by_title(book=Depends(get_from_db_by_title)):
    return book


@app.post("/books/{title}/mod/")
def change_author_of_book_with_title(
    new_author: str,
    book=Depends(get_from_db_by_title),
):
    book.author = new_author

    return book
