import pytest
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine
# from schemas

client = TestClient(app)

url = 'postgresql://postgres:9792amina@localhost:5432/midterm'
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


def test_get_books_by_price(test_db):
    response = client.get("/books_by_price")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_books(test_db):
    response = client.get("/all_books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_genres(test_db):
    response = client.get("/all_genres")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_publishers(test_db):
    response = client.get("/all_publishers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_user(test_db):
    user_data = {"username": "new_user", "password": "new_password"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["greeting"] == "new_user"


def test_login(test_db):
    user_data = {"username": "existing_user", "password": "existing_password"}
    client.post("/users", json=user_data)
    login_data = {"username": "existing_user", "password": "existing_password"}
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_user(test_db):
    user_data = {"username": "user_for_me", "password": "password_for_me"}
    client.post("/users", json=user_data)
    login_data = {"username": "user_for_me", "password": "password_for_me"}
    login_response = client.post("/login", json=login_data)
    token = login_response.json()["access_token"]
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "user_for_me"


def test_add_book(test_db):
    book_data = {"title": "New Book", "desc": "asdfg", "author": "New Author", "price": 100, "genre_id": 1, "publisher_id": 1}
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    assert response.text == '"New Book"'


def test_add_publisher(test_db):
    publisher_data = {"name": "New Publisher", "address": "New Address"}
    response = client.post("/publishers", json=publisher_data)
    assert response.status_code == 200
    assert response.text == '"New Publisher"'


def test_add_genre(test_db):
    genre_data = {"name": "New Genre"}
    response = client.post("/genres", json=genre_data)
    assert response.status_code == 200
    assert response.text == '"New Genre"'


def test_add_order(test_db):
    order_data = {"user_id": 1, "total_price": 1000.0, "status": "active"}
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
