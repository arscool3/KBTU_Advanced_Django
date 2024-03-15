import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

# from database import engine
from models import ModelBase

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


@pytest.fixture
def test_db():
    ModelBase.metadata.create_all(bind=engine)
    yield
    ModelBase.metadata.drop_all(bind=engine)


def test_get_genre(test_db):
    response = client.get("/genre/")
    print(response.json())
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre/", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genre/")
    assert response.json() == [{'id': 1, 'name': 'drama'}]


def test_get_movie(test_db):
    response = client.get("/movie/")
    print(response.json())
    assert response.json() == []


def test_get_director(test_db):
    response = client.get("/director/")
    print(response.json())
    assert response.json() == []


def test_add_director(test_db):
    response = client.post("/director/", json={'name': 'Danila'})
    assert response.status_code == 200
    response = client.get("/director/")
    assert response.json() == [{'id': 1, 'name': 'Danila'}]


def test_add_movie(test_db):
    client.post("/director/", json={'name': 'Danila'})
    response = client.post("/movie/", json={
        "name": "Movie",
        "director_id": 1
    })
    assert response.status_code == 200
    response = client.get("/movie/")
    assert response.json() == [
        {
            "id": 1,
            "name": "Movie",
            "director": {
                "id": 1,
                "name": "Danila"
            },
            "genres": []
        }
    ]
