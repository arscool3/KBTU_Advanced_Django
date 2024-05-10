import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import schemas
import models
from database import Base
from main import app, get_db

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


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get(test_db):
    assert True


def test_get_employers(test_db):
    response = client.get("/employers")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_add_employer(test_db):
    new_employer = {"name": "Test Company", "location": "A test location."}

    response = client.post("/employers", json=new_employer)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_employer["name"]
    assert "id" in data

    with get_test_db() as db:
        employer = db.query(models.Employer).filter(models.Employer.name == "Test Company").first()
        assert employer is not None


def test_get_jobs(test_db):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 0


def test_add_job(test_db):
    new_job = {
        "title": "Test Job Title",
        "location": "Test Job Location",
        "salary": 500000,
        "time": "full-time",
        "years_of_experience": 3,
        "employer_id": 1
    }

    response = client.post("/jobs", json=new_job)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_job["title"]
    assert "id" in data

    with get_test_db() as db:
        job = db.query(models.Job).filter(models.Job.title == "Test Job Title").first()
        assert job is not None
        assert job.description == "Test Job Description"


def test_get_candidate_by_id(test_db):
    candidate_id = 1
    response = client.get(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == candidate_id
    assert 'name' in data
    assert 'age' in data

    expected_name = "Test Candidate"
    expected_age = 20
    assert data['name'] == expected_name
    assert data['age'] == expected_age


def test_add_candidate(test_db):
    new_candidate = {
        "name": "Test Candidate",
        "age": 20
    }
    response = client.post("/candidates", json=new_candidate)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_candidate["name"]
    assert "id" in data

    with test_db() as db:
        candidate = db.query(models.Candidate).filter(models.Candidate.name == "Test Candidate").first()
        assert candidate is not None
        assert candidate.age == new_candidate["age"]


def test_get_all_skills(test_db):
    response = client.get("/skills")
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)


def test_add_skill(test_db):
    new_skill = {"title": "Python"}
    response = client.post("/skills", json=new_skill)
    assert response.status_code == 200
    skill_data = response.json()
    assert skill_data["title"] == new_skill["title"]

    with test_db() as db:
        skill = db.query(models.Skill).filter(models.Skill.title == "Python").first()
        assert skill is not None
        assert skill.title == new_skill["title"]


def test_get_skill_by_title(test_db):
    skill_title = "Python"
    response = client.get(f"/skills/{skill_title}")
    assert response.status_code == 200
    skill = response.json()
    assert skill['title'] == skill_title


def test_add_resume_to_candidate(test_db):
    new_resume = {
        "title": "Software Developer",
        "candidate_id": 1,
        "location": "New York",
        "education": "B.Sc. Computer Science",
        "years_of_experience": 5
    }
    response = client.post("/candidates/resumes", json=new_resume)
    assert response.status_code == 200
    assert "New resume was added to candidate" in response.content.decode()


def test_get_candidate_resumes(test_db):
    candidate_id = 1
    response = client.get(f"/candidates/resumes?id={candidate_id}")
    assert response.status_code == 200
    resumes = response.json()
    assert isinstance(resumes, list)
    assert any(resume["candidate_id"] == candidate_id for resume in resumes)
