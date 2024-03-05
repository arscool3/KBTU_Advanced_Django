import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from database import Base, engine

client = TestClient(app)
url = 'postgresql://postgres:Dimash2003@localhost:5432/test_adv_django'
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


def test_get_film(test_db):
    response = client.get("/film")
    assert response.json() == []


def test_add_film(test_db):
    response = client.post("/film", json={'name': 'drama', 'director_id': 1, 'genre_id': 1})
    assert response.status_code == 200
    response = client.get("/film")
    assert response.json() == [{'id': 1, 'name': 'drama', 'director_id': 1, 'genre_id': 1}]


def test_get_director(test_db):
    response = client.get("/director")
    assert response.json() == []


def test_add_director(test_db):
    response = client.post("/director", json={'name': 'Christopher Nolan'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'name': 'Christopher Nolan'}]
