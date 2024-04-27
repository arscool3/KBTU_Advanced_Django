from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class Literature(BaseModel):
    title: str
    author: str
    

class Book(Literature):
    pass


class Magazine(Literature):
    pass


literatures =[]

def add_book_dep(literature: Annotated[Book, Magazine])-> str:
    literatures.append(literature)
    return f"{literature} was added"

@app.post('/literature')
def add_book(book_dep: str=Depends(add_book_dep))-> str:
    return book_dep

@app.post('/literature/edit')
def edit_literature_title(title: str,literature_dep: str=Depends(add_book_dep)):
    pass