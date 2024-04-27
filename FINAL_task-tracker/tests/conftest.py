import pytest
import sqlalchemy
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import config
from main import app
from database import engine, get_db, Base
from projects import schemas
from projects.models import Project
from projects.schemas import CreateProject
from users.models import User

url = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/test_midka_django'
engine = sqlalchemy.create_engine(url)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    db = test_session()
    try:
        yield db
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_session


@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def project():
    session = test_session()
    project = {
        "id": 1000,
        "name": "test_project",
        "description": "",
    }
    session.add(Project(**project))
    session.commit()

    return project


@pytest.fixture
def user(project):
    session = test_session()
    user = {
        "id": 1000,
        "first_name": "test_user",
        "last_name": "test_user",
        "email": "test@example.com",
        "project_id": project["id"],
    }
    session.add(User(**user))
    session.commit()
    return user

