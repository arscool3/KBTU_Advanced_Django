import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = sqlalchemy.create_engine(url)
test_session = Session(engine)


def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise
    finally:
        test_session.close()


app.dependency_overrides[get_db] = get_test_db


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


def test_get_director(test_db):
    response = client.get("/director")
    assert response.json() == []


def test_add_director(test_db):
    response = client.post("/director", json={'name': 'Askhat'})
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'Askhat'}]

def test_get_film(test_db):
    response = client.get("/films")
    assert response.json() == []


def test_add_film(test_db):
    response = client.post("/films", json={'name': 'Avatar'})
    assert response.status_code == 200
    response = client.get("/films")
    assert response.json() == [{'id': 1, 'name': 'Avatar'}]