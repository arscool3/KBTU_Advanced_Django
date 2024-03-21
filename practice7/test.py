import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
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

def test_get_films(test_db):
    response = client.get("/films")
    assert response.json() == []

def test_add_films(test_db):
    response = client.post("/films", json = {'name':'1+1','director_id': '1', 'genre_id': '1' })
    assert response.status_code == 200
    response = client.get("/films")
    assert response.json() == [{'id': 1,'name':'1+1','director_id': '1', 'genre_id': '1'}]

def test_get_director(test_db):
    response = client.get("/directors")
    assert response.json() == []

def test_add_director(test_db):
    response = client.post("/directors", json = {'name':'Kevin F'})
    assert response.status_code == 200
    response = client.get("/directors")
    assert response.json() == [{'id': 1,'name':'Kevin F'}]
 


