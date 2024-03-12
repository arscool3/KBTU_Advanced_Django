import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database import Base
from main import app, get_db

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5436/postgres'
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


def test_get_user(test_db):
    response = client.get("/users")
    assert response.status_code == 200
    assert (response.json() == [])


def test_add_user(test_db):
    response = client.post("/users", json={'name': 'Julia'})
    assert response.status_code == 200
    response = client.get("/users")
    assert response.json() == [{'id': 1, 'name': 'Julia'}]


def test_get_projects(test_db):
    response = client.get("/projects")
    assert response.status_code == 200
    assert (response.json() == [])


def test_get_assignment(test_db):
    response = client.get("/task_assignments")
    assert response.status_code == 200
    assert (response.json() == [])


def test_add_assignment(test_db):
    response = client.post("/task_assignments", json={'name': 'Ass1'})
    assert response.status_code == 200
    response = client.get("/task_assignments")
    assert response.status_code == 200
    assignments = response.json()
    assert assignments[0]['name'] == 'Ass1'


def test_get_report(test_db):
    response = client.get("/reports")
    assert response.status_code == 200
    assert (response.json() == [])


def test_add_report(test_db):
    response = client.post("/reports", json={'name': 'Report for Music'})
    assert response.status_code == 200
    response = client.get("/reports")
    assert response.json() == [{'id': 1, 'name': 'Report for Music'}]


def test_get_status(test_db):
    response = client.get("/task_statuses")
    assert response.status_code == 200
    assert (response.json() == [])


def test_get_tasks(test_db):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert (response.json() == [])


def test_add_task(test_db):
    project_name = 'Games'
    user_name = 'Vova'

    response = client.post("/tasks", json={'name': 'Game'},
                           params={'project_name': project_name, 'user_name': user_name})

    assert response.status_code == 200
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    print(tasks)
    assert tasks[0]['name'] == 'Game'

