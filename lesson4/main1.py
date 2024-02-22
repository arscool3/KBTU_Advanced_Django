from http.client import HTTPException

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

class BorrowRequest(BaseModel):
    user_name: str
    book_title: str

available_books = [
    {"title": "1984", "author": "George Orwell"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

def check_for_eligibility(borrow_request: BorrowRequest):
    if borrow_request.user_name.startswith('T'):
        raise HTTPException(status_code=400, detail="User is not eligible to borrow books.")
    return borrow_request

def check_book_availability(borrow_request: BorrowRequest = Depends(check_for_eligibility)):
    for book in available_books:
        if book['title'] == borrow_request.book_title:
            return f"Book '{borrow_request.book_title}' by {book['author']} is available for borrowing."
    return f"Sorry, the book '{borrow_request.book_title}' is not available right now."

@app.post("/borrrow_book")
def borrow_book(message: str = Depends(check_book_availability)):
    return {"message": message}

# create 1 handler with nested dependency