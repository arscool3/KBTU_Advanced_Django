import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from utils.database import get_db, Base

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


def test_get_all_users(test_db):
    response = client.get('/all-users')
    assert response.json() == []


def test_get_post_by_id(test_db):
    response = client.get('posts/1')
    if response.status_code == 200:
        assert response.json()['id'] == 1
    elif response.status_code == 404:
        assert response.json() == {'detail': 'Post not found'}
    else:
        assert False, f"Unexpected response status code: {response.status_code}"


def test_register_valid_user():
    response = client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.text == "User created"


def test_register_existing_user():
    response = client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400
    assert "User already exists" in response.text


def test_login_valid_credentials():
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_username():
    response = client.post("/login", data={"username": "invaliduser", "password": "testpassword"})
    assert response.status_code == 401
    assert "Invalid user credentials" in response.text


def test_get_home():
    response = client.get("/home", headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 200
    assert "Hello user" in response.text


def test_create_post():
    response = client.post("/posts", json={"title": "Test Post", "content": "Test Content"},
                           headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 200
    assert "Post created" in response.text


def test_get_posts():
    response = client.get("/posts", headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_comments():
    response = client.get("/profile/comments", headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
