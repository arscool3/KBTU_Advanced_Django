import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app, get_db
from database import engine
from database import Base

client = TestClient(app)

url = 'postgresql://postgres:December1225@localhost:5432/midterm_2'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


def test_get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


app.dependency_overrides[get_db] = test_get_db


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_users(test_db):
    response = client.get("/users/")
    assert response.json() == []


def test_add_user(test_db):
    response = client.post("/users/", json={'name': 'Lera', 'email': 'leralera'})
    assert response.status_code == 200
    response = client.get("/users/")
    assert response.json() == [{'id': 1, 'name': 'Lera', 'email': 'leralera', 'cart': None}]


def test_get_firms(test_db):
    response = client.get("/firms/")
    assert response.json() == []


def test_add_firm(test_db):
    response = client.post("/firms/", json={'name': 'Lera', 'description': 'leralera'})
    assert response.status_code == 200
    response = client.get("/firms/")
    assert response.json() == [{'id': 1, 'name': 'Lera', 'description': 'leralera'}]


def test_get_categories(test_db):
    response = client.get("/categories/")
    assert response.json() == []


def test_add_category(test_db):
    response = client.post("/categories/", json={'name': 'Lera', 'description': 'leralera'})
    assert response.status_code == 200
    response = client.get("/categories/")
    assert response.json() == [{'id': 1, 'name': 'Lera', 'description': 'leralera'}]


def test_get_products(test_db):
    response = client.get("/products/")
    assert response.json() == []


def test_add_product(test_db):
    response = client.post("/products/", json={'name': 'Lera', 'description': 'leralera', 'price': 123, 'category_id': 1, 'firm_id': 1})
    assert response.status_code == 200
    response = client.get("/products/")
    assert response.json() == [{'id': 1, 'name': 'Lera', 'description': 'leralera', 'price': 123}]


def test_get_carts(test_db):
    response = client.get("/carts/")
    assert response.json() == []


def test_add_cart(test_db):
    response = client.post("/carts/", json={'user_id': 1})
    assert response.status_code == 200
    response = client.get("/carts/")
    assert response.json() == [{'id': 1, 'user_id': 1}]


def test_get_cart_items(test_db):
    response = client.get("/cart_items/")
    assert response.json() == []


def test_add_cart_items(test_db):
    response = client.post("/cart_items/", json={'amount': 1, 'cart_id': 1, 'product_id': 1})
    assert response.status_code == 200
    response = client.get("/cart_items/")
    assert response.json() == [{'id': 1, 'amount': 1, 'cart_id': 1, 'product_id': 1}]

