from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

class BorrowRequest(BaseModel):
    user_name: str
    book_title:str

available_books = [
    {"title": "1984", "author": "Georgie Orwell"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

def check_book_availability(borrow_request: BorrowRequest):
    for book in available_books:
        if book['title'] == borrow_request.book_title:
            return f"Book '{borrow_request.book_title}' by {book['author']} is available for you, {borrow_request.user_name}!"
    return f"Sorry, the book '{borrow_request.book_title}' is not available right now."

@app.post("/borrow_book")
def borrow_book(message: str = Depends(check_book_availability)):
    return {"message": message}
# 1 handler and 1 Function that is injected as DI
