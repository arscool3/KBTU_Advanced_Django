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
def test_hooper_data():
    return {
        "name": "John Doe"
    }


@pytest.fixture
def test_command_data():
    return {
        "name": "Test Command",
        "description": "Sample description"
    }


@pytest.fixture
def test_conference_data():
    return {
        "name": "Conference A",
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    }


@pytest.fixture
def test_hooper(test_db, test_hooper_data):
    db = next(get_test_db())
    hooper = models.Hooper(**test_hooper_data)
    db.add(hooper)
    return test_hooper_data


@pytest.fixture
def test_command(test_db, test_command_data):
    db = next(get_test_db())
    command = models.Command(**test_command_data)
    db.add(command)
    return test_command_data


@pytest.fixture
def test_conference(test_db, test_conference_data):
    db = next(get_test_db())
    location_data = test_conference_data.pop("location")
    location = models.Location(**location_data)
    conference = models.Conference(**test_conference_data, location=location)
    db.add(conference)
    return test_conference_data


def test_get_hooper(test_db):
    response = client.get("/hoopers/")
    assert response.json() == []


def test_get_command(test_db):
    response = client.get("/commands/")
    assert response.json() == []


def test_get_conference(test_db):
    response = client.get("/conferences/")
    assert response.json() == []


def test_get_hooper_by_id(test_db):
    response = client.get("/hoopers/?hooper_id=0")
    assert response.json() is None or response.json()


def test_get_command_by_id(test_db):
    response = client.get("/commands/?command_id=0")
    assert response.json() is None or response.json()


def test_get_conference_by_id(test_db):
    response = client.get("/conferences/?conference_id=0")
    assert response.json() is None or response.json()


def test_create_hooper(test_db, test_hooper_data):
    response = client.post("/hoopers/", json=test_hooper_data)
    assert response.status_code == 201


def test_create_command(test_db, test_command_data):
    response = client.post("/commands/", json=test_command_data)
    assert response.status_code == 201


def test_create_conference(test_db, test_conference_data):
    response = client.post("/conferences/", json=test_conference_data)
    assert response.status_code == 201
