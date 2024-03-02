from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from main import app, get_db
from database import Base

client = TestClient(app)

# New Test db
url = 'postgresql://postgres:postgres@localhost:5436/postgres'
engine = create_engine(url)
test_session = Session(engine)


def override_get_session():
    try:
        yield test_session
    finally:
        test_session.close()

app.dependency_overrides[get_db] = override_get_session

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_genre(test_db):
    response = client.get("/genres")
    assert response.status_code == 200
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genres")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'drama'}]


# Practice
# Add 4 tests (2 for director, 2 film)

def test_add_director(test_db):
    response = client.post("/director", json={"name": "Charlie Devis"})
    assert response.status_code == 200
    response = client.get("/directors")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Charlie Devis'}]


def test_get_directors(test_db):
    response = client.get("/directors")
    assert response.status_code == 200
    assert response.json() == []


def test_get_films(test_db):
    response = client.get("/films")
    assert response.status_code == 200
    assert response.json() == []


def test_add_films(test_db):
    response_director = client.post("/director", json={"name": "Steven Spielberg"})
    assert response_director.status_code == 200

    response_genre = client.post("/genre", json={'name': 'Action'})
    assert response_genre.status_code == 200

    film_data = {
        "director_id": 1,
        "genre_id": 1,
        "name": "Jurassic Park"
    }

    response_film = client.post("/film", json=film_data)
    assert response_film.status_code == 200
    response_films = client.get("/films")
    assert response_films.status_code == 200
    assert response_films.json() == [{'id': 1, 'director_id': 1, 'genre_id': 1, 'name': 'Jurassic Park'}]
