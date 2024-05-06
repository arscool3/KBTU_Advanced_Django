import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine
from schemas import CreateGenre

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
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


def test_get_film(test_db):
    response = client.get("/film")
    assert response.json()==[]

def test_add_ilms(test_db):
    response = client.post("/film", json= {'name': "everything everytwhere all at once"} )
    assert response.status_code == 200
    response = client.get("/film")
    assert response.json() == [{"id":1, "name": "everything everywhere ll at once"}]

def test_get_directors(test_db):
    response = client.get("/director")
    assert response.json()==[]

def test_add_directors(test_db):
    response = client.post("/director", json= {'name': "uhhhhh greta gerwig"} )
    assert response.status_code == 200
    response = client.get("/director")
    assert response.json() == [{"id":1, "name": "greta gerwig"}]

