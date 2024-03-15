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
def test_artist_data():
    return {
        "name": "RHCP"
    }

@pytest.fixture
def test_song_data():
    return {
        "name": "Under the bridge",
        "artist_id": "1"
    }

@pytest.fixture
def test_artist(test_db, test_artist_data):
    db = next(get_test_db())
    artist = models.Artist(**test_artist_data)
    db.add(artist)
    return test_artist_data

@pytest.fixture
def test_song(test_db, test_song_data):
    db = next(get_test_db())
    song = models.Song(**test_song_data)
    db.add(song)
    return test_song_data


def test_get_artist(test_db):
    response = client.get("/artists/")
    assert response.json() == []


def test_get_song(test_db):
    response = client.get("/songs/")
    assert response.json() == []


def test_get_artist_by_id(test_db):
    response = client.get("/artists/?artist_id=0")
    assert response.json() is None or response.json()


def test_get_song_by_id(test_db):
    response = client.get("/songs/?song_id=0")
    assert response.json() is None or response.json()


def test_create_artist(test_db, test_artist_data):
    response = client.post("/artists/", json=test_artist_data)
    assert response.status_code == 201