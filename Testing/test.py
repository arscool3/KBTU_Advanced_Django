import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import engine
from models import Base

# from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:December1225@localhost:5432/test_lesson_7'
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


def test_get_genre(test_db):
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
    response = client.post("/director", json={'name': 'AAA '})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'AAA '}]


def test_get_movie(test_db):
    response = client.get("/movie")
    assert response.json() == []


def test_add_movie(test_db):
    response = client.post("/movie", json={'name': 'SSS', "director_id": 1, "genre_id": 1})
    assert response.status_code == 200
    response = client.get("/movie")
    assert len(response.json()) == 1
