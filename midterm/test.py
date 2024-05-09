import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db
from database import Base, engine

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5432/midtermm'
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


def test_get_item(test_db):
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_seller(test_db):
    response = client.get("/sellers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customers(test_db):
    response = client.get("/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_orders(test_db):
    response = client.get("/order")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_shops(test_db):
    response = client.get("/shops")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_director(test_db):
    response = client.get("/favorites")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_item(test_db):
    response = client.post("/items", json={
      "name": "bag",
      "price": 25000,
      "description": "fvrtvgrgvrvrt",
      "rating": 3
    })
    assert response.status_code == 200
    response = client.get("/items")
    assert response.json() == [{
        "id": 1,
        "name": "bag",
        "price": 25000,
        "description": "fvrtvgrgvrvrt",
        "rating": 3
    }]


def test_add_seller(test_db):
    response = client.post("/seller", json={'name': 'John'})
    assert response.status_code == 200
    response = client.get("/sellers")
    assert response.json() == [{'id': 1, 'name': 'John'}]


def test_add_customer(test_db):
    response = client.post("/customer", json={'name': 'John'})
    assert response.status_code == 200
    response = client.get("/customers")
    assert response.json() == [{'id': 1, 'name': 'John'}]

