import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app,get_db

from database import Base, engine
from schemas import CreateGenre
url='postgresql://postgres:aru@localhost:5433/test_postgres'

engine=sqlalchemy.create_engine(url)
session=Session(engine)
client=TestClient(app)
test_session=Session(engine)
@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise
    finally:
        test_session.close()    

app.dependency_orverrides[get_db]=get_test_db
def test_get_genre(test_db):
    response = client.get("/genre")
    assert response.json() == []


def test_add_genre(test_db):
    response = client.post("/genre", json={'name': 'drama'})
    assert response.status_code == 200
    response = client.get("/genre")
    assert response.json() == [{'id': 1, 'name': 'drama'}] 

