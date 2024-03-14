import pytest
import sqlalchemy
from sqlalchemy.orm import Session, declarative_base

from fastapi.testclient import TestClient
from main import app

from database import engine

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)

Base = declarative_base()

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_add_category(test_db):
    response = client.post("/categories", json={
  "name": "Tests",
  "photo_url": "Tests"
})
    assert response.status_code == 200
    assert response.json() == "Category was added"


def test_get_category_list(test_db):
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_product(test_db):
    product_data = {
        "name": "Tests",
        "price": 0,
        "description": "string",
        "photo_url": "string",
        "category_id": 0
    }
    
    response = client.post("/products", json=product_data) 
    assert response.status_code == 200
    assert response.json() == "Products was added"

def test_get_products_by_category(test_db):
    response = client.get("/products/1")  
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_details(test_db):
    response = client.get("/product/1")  
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_create_user(test_db):
    user_data = {
        "username": "test_users"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json() == "User was added"

def test_get_users(test_db):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

