import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:Haker15987@localhost:5432/postgres4'
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
    response = client.post("/genre", json={'name': 'comedy'})
    assert response.status_code == 200
    response = client.get("/genre")
    assert response.json() == [{'id': 1, 'name': 'comedy'}]


def test_add_director(test_db):
    response = client.post("/director", json={'name': 'Saule'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'Saule'}]


def test_add_film(test_db):
    client.post("/genre", json={'name': 'fiction'})
    client.post("/director", json={"name": "Alisa"})
    response = client.post("/film", json={
        "name": "Dune2",
        "description": "Sand",
        "rating": 10.0,
        "duration": 180,
        "director_id": 1,
        "genre_id": 1,
    })
    assert response.status_code == 200
    response = client.get("/film")
    expected_response = [{
        'id': 1,
        'name': 'Dune2',
        'description': 'Sand',
        'rating': 10.0,
        'duration': 180,
        'directors': {'id': 1, 'name': 'Alisa'},
        'genres': {'id': 1, 'name': 'fiction'}
    }]
    assert response.json() == expected_response


def test_get_film(test_db):
    response = client.get("/film")
    assert response.json() == []


def test_get_director(test_db):
    response = client.get("/director")
    assert response.json() == []