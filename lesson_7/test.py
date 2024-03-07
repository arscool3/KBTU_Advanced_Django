import pytest

from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from database import Base, engine

client = TestClient(app)

url = 'postgresql://postgres:admin@localhost:5433/test_postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_genre():
    response = client.get("/genre")
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genre")
    assert response.json() == [{'id': 1, 'name': 'drama'}]


def test_get_director(test_db):
    response = client.get("/director")
    assert response.json() == []


def test_add_director(test_db):
    response = client.post("/director", json={'name': 'Christopher Nolan'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'Christopher Nolan'}]


def test_get_film(test_db):
    response = client.get("/film")
    assert response.json() == []


def test_add_film(test_db):
    response = client.post("/film", json={'name': 'Tennet', 'director_id': 1, 'genre_id': 1})
    assert response.status_code == 200
    response = client.get("/film")
    assert response.json() == [{'id': 1, 'name': 'Tennet', 'director_id': 1, 'genre_id': 1}]
