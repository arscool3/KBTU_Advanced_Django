from python import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:601246@localhost:5432/lesson7'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_genre(test_db):
    response = client.get("/genre")
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genre")
    assert response.json() == [{'id': 1, 'name': 'drama'}]


def test_add_director(test_db):
    response = client.post("/director", json={'name': 'John'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'John'}]


def test_add_film(test_db):
    client.post("/genre", json={'name': 'horror'})
    client.post("/director", json={"name": "Lisa"})
    response = client.post("/film", json={
        "name": "Meg",
        "description": "hjvbhvbhvh",
        "rating": 6.7,
        "duration": 120,
        "director_id": 1,
        "genre_id": 1,
    })
    assert response.status_code == 200
    response = client.get("/film")
    assert response.json() == [{'id': 1, 'name': 'Meg'}]


def test_get_film(test_db):
    response = client.get("/film")
    assert response.json() == []


def test_get_director(test_db):
    response = client.get("/director")
    assert response.json() == []