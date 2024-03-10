import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from database import Base

client = TestClient(app)

url = 'postgresql://postgres:Haker15987@localhost/test'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    session.begin()
    yield
    session.rollback()
    Base.metadata.drop_all(bind=engine)


def test_get_all_courses(test_db):
    response = client.get("/all_courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_users(test_db):
    response = client.get("/all_users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_user(test_db):
    response = client.post("/users", json={"name": "John", "email": "john@gmail.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == "User added"


def test_add_course(test_db):
    response = client.post("/courses",
                           json={"title": "Advanced Django Course", "description": "Learn Fast Api", "price": 100})
    assert response.status_code == 200
    assert response.json() == "Course added"


def test_add_video(test_db):
    response = client.post("/videos", json={"title": "Introduction to Fast Api", "url": "http://example.com/video",
                                            "course_id": 1})
    assert response.status_code == 200
    assert response.json() == "Video added"


def test_add_review(test_db):
    response = client.post("/reviews", json={"content": "Great course!", "course_id": 1, "user_id": 1})
    assert response.status_code == 200
    assert response.json() == "Review added"


def test_add_purchase(test_db):
    response = client.post("/purchases", json={"user_id": 1, "course_id": 1, "purchase_date": "2022-01-01"})
    assert response.status_code == 200
    assert response.json() == "Purchase added and course associated with user"

#
def test_get_user_courses():
    response = client.get("/users/1/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_course_users(test_db):
    response = client.get("/courses/1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
#
def test_add_progress(test_db):
    response = client.post("/progress", json={"completion_percentage": 10, "course_id": 1, "user_id": 1})
    assert response.status_code == 200
    assert response.json() == "Progress added"
