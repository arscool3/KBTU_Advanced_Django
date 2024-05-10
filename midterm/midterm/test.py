import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app, get_db
from database import Base

client = TestClient(app)

url = 'postgresql://postgres:Dimash2003@localhost:5432/midterm_adv_django'
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


def test_add_user(client):
    response = client.post("/users", json={"username": "test_user", "password": "password"})
    assert response.status_code == 200
    assert response.json()["message"] == "User added successfully"
    response = client.post("/users", json={"username": "test_user2", "password": ""})
    assert response.status_code == 200
    assert response.json()["message"] == "Password is empty"


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    response = client.delete("/users/999")
    assert response.status_code == 404


def test_get_post_comments(client):
    response = client.get("/comments/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/comments/999")
    assert response.status_code == 500
