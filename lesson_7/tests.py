import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from main import app

from database import engine, get_db
from models import Base
from schemas import CreateGenre
import config

client = TestClient(app)

url = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/test_lesson_7'
engine = sqlalchemy.create_engine(url)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    db = test_session()
    try:
        yield db
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_session

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
    response = client.post("/director", json={"name": "dir"})
    assert response.status_code == 200
    response = client.get("/directors")
    assert response.json() == [{'id': 1, 'name': 'dir'}]


def test_get_directors(test_db):
    response = client.get("/directors")
    assert response.status_code == 200
    assert response.json() == []


def test_add_movie(test_db):
    response = client.post("/film", json={
        "director_id": 1,
        "genre_id": 1,
        "name": "string"
    })
    assert response.status_code == 200
    response = client.get("/films")
    assert response.status_code == 200


def test_get_movie(test_db):
    response = client.get("/films")
    assert response.status_code == 200
