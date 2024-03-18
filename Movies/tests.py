import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine

client = TestClient(app)

test_url = 'postgresql://postgres:password@localhost:5434/postgres'
engine = sqlalchemy.create_engine(test_url)
test_session = Session(engine)


# docker run --name test_movie -e POSTGRES_PASSWORD=password -p 5434:5432 postgres


def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise NotImplementedError()
    finally:
        test_session.close()


app.dependency_overrides[get_db] = get_test_db


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
    response = client.post("/director", json={'name': 'Somebody'})
    assert response.status_code == 200

    response = client.get("/director")
    assert response.json() == [{'id': 1, 'name': 'Somebody'}]


def test_get_films(test_db):
    response = client.get("/director")
    assert response.json() == []


def test_add_film(test_db):
    test_add_director(test_db)
    test_add_genre(test_db)

    response = client.post("/film", json={
        'director_id': 1,
        'genre_id': 1,
        'name': 'Somebody'
    })
    assert response.status_code == 200
