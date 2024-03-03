import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:9792amina@localhost:5432/lesson_7'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_genres(test_db):
    response = client.get("/genre")
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genre")
    assert response.json() == [{'id': 1, 'name': 'drama'}]

def test_get_directors(test_db):
    response = client.get("/director")
    assert response.json() == []

def test_add_director(test_db):
    response = client.post("/director", json={'name': 'Sam'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 2, 'name': 'Sam'}]


def test_get_films(test_db):
    response = client.get("/film")
    assert response.json() == []

def test_add_film(test_db):
    client.post("/genre", json={'name': 'fantasy'})
    client.post("/director", json={"name": "Tom"})
    response = client.post("/film", json={
        "name": "Home",
        "description": "asdfghj",
        "rating": 5,
        "duration": 140,
        "director_id": 3,
        "genre_id": 2,
    })
    assert response.status_code == 200
    response = client.get("/film")
    assert response.json() == [{'id': 3, 'name': 'Home'}]