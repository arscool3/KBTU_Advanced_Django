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
    response = client.post("/users", json={"name": "Aruzhan", "description": "Likes to read"})
    assert response.status_code == 200
    assert response.text == "User was added"

def test_get_all_users(test_db):
    client.post("/users", json={"name": "Diana", "description": "Likes books about GameDev"})
    client.post("/users", json={"name": "Aisha", "description": "Likes to read about hiking"})

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_create_genre(test_db):
    response = client.post("/genres", json={"name": "Horror", "description": "Makes you afraid of everything normal"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Horror", "description": "Makes you afraid of everything normal"}

def test_get_all_genres(test_db):

    client.post("/genres", json={"name": "Horror", "description": "Makes you afraid of everything normal"})
    client.post("/genres", json={"name": "Science Fiction", "description": "Explores futuristic concepts"})
    

    response = client.get("/genres")
    assert response.status_code == 200
    assert len(response.json()) == 2
    

    assert {"id": 1, "name": "Horror", "description": "Makes you afraid of everything normal"} in response.json()
    assert {"id": 2, "name": "Science Fiction", "description": "Explores futuristic concepts"} in response.json()


def test_create_book(test_db):
    response = client.post("/books", json={"name": "Lolita", "description": "Is a very strange book...", "author_id": 1, "genre_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Lolita", "description": "Is a very strange book...", "author_id": 1, "genre_id": 1}


def test_create_author(test_db):
    response = client.post("/authors", json={"name": "Nabokov", "description": "Is a very strange man..."})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Nabokov", "description": "Is a very strange man"}


def test_create_quote(test_db):
    response = client.post("/quotes", json={"description": "Everything else is rust and stardust", "author_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "description": "Everything else is rust and stardust", "author_id": 1}


def test_create_book_review(test_db):
    response = client.post("/bookreviews", json={"review": "Why would anyone write something like that...Nabokov is a very weird man...Liked the book though", "rating": 5, "user_id": 1, "book_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "review": "Why would anyone write something like that...Nabokov is a very weird man...Liked the book though", "rating": 5, "user_id": 1, "book_id": 1}

def test_get_books_by_author_id(test_db):

    response = client.post("/authors", json={"name": "J.R.R. Tolkien", "description": "Author of The Lord of the Rings"})
    assert response.status_code == 200
    author_id = response.json()["id"]
    
    client.post("/books", json={"name": "The Hobbit", "description": "Fantasy novel", "author_id": author_id, "genre_id": 1})
    client.post("/books", json={"name": "The Lord of the Rings", "description": "Epic fantasy series", "author_id": author_id, "genre_id": 1})
    
    response = client.get(f"/books?author_id={author_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_quotes_by_author_id(test_db):

    response = client.post("/authors", json={"name": "Ernest Hemingway", "description": "Famous American novelist"})
    assert response.status_code == 200
    author_id = response.json()["id"]

    client.post("/quotes", json={"description": "Courage is grace under pressure", "author_id": author_id})
    client.post("/quotes", json={"description": "The only thing that could spoil a day was people", "author_id": author_id})

    response = client.get(f"/quotes?author_id={author_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2
    

    assert {"description": "Courage is grace under pressure", "author_id": author_id} in response.json()
    assert {"description": "The only thing that could spoil a day was people", "author_id": author_id} in response.json()
