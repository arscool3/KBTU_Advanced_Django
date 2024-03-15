import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:aru@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
test_session = Session(engine)


def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise
    finally:
        test_session.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    response = client.post("/users", json={"name": "John Doe", "description": "A user from Goodreads"})
    assert response.status_code == 200
    assert response.text == "User was added"


def test_create_genre(test_db):
    response = client.post("/genres", json={"name": "Fantasy", "description": "Genre for fantasy books"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Fantasy", "description": "Genre for fantasy books"}


def test_create_book(test_db):
    response = client.post("/books", json={"name": "Book Name", "description": "Description of the book", "author_id": 1, "genre_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Book Name", "description": "Description of the book", "author_id": 1, "genre_id": 1}


def test_create_author(test_db):
    response = client.post("/authors", json={"name": "Author Name", "description": "Description of the author"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Author Name", "description": "Description of the author"}


def test_create_quote(test_db):
    response = client.post("/quotes", json={"description": "Quote description", "author_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "description": "Quote description", "author_id": 1}


def test_create_book_review(test_db):
    response = client.post("/bookreviews", json={"review": "Book review", "rating": 5, "user_id": 1, "book_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "review": "Book review", "rating": 5, "user_id": 1, "book_id": 1}

