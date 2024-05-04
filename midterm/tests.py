import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

import models

from database import get_db
from models import ModelBase

client = TestClient(app)

url = 'postgresql://postgres:password@postgres-test:5433/postgres'
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
    ModelBase.metadata.create_all(bind=engine)
    yield
    ModelBase.metadata.drop_all(bind=engine)


@pytest.fixture
def test_mark_data():
    return {
        "name": "MARK1"
    }


@pytest.fixture
def test_person_data():
    return {
        "iin": "000000000000",
        "name": "Test",
        "surname": "Testovich"
    }


@pytest.fixture
def test_mark(test_db, test_mark_data):
    db = next(get_test_db())
    mark = models.Mark(**test_mark_data)
    db.add(mark)
    return test_mark_data


@pytest.fixture
def test_person(test_db, test_person_data):
    db = next(get_test_db())
    person = models.Person(**test_person_data)
    db.add(person)
    return test_person_data


def test_get_marks(test_db):
    response = client.get("/marks/")
    assert response.json() == []


def test_add_mark(test_db, test_mark_data):
    response = client.post("/marks/", json=test_mark_data)
    assert response.status_code == 200
    assert response.json() == test_mark_data["name"]

    response = client.get("/marks/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_remove_mark(test_db, test_mark):
    response = client.get("/marks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    mark_id = response.json()[0]["id"]

    response = client.delete("/marks/?mark_id={}".format(mark_id))
    assert response.status_code == 200
    assert response.json() == "Deleted"

    response = client.get("/marks/")
    assert response.status_code == 200
    assert response.json() == []


def test_add_person(test_db, test_person_data):
    response = client.post("/person/", json=test_person_data)
    assert response.status_code == 200
    assert response.json() == test_person_data["iin"]

    response = client.get("/person/?iin={}".format(test_person_data["iin"]))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["iin"] == test_person_data["iin"]
    assert response_json["name"] == test_person_data["name"]
    assert response_json["surname"] == test_person_data["surname"]


def test_add_test_person_same_iin(test_db, test_person_data, test_person):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        client.post("/person/", json=test_person_data)


def test_get_person_by_id(test_db, test_person):
    response = client.get("/person/?iin={}".format(test_person["iin"]))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["iin"] == test_person["iin"]
    assert response_json["name"] == test_person["name"]
    assert response_json["surname"] == test_person["surname"]
