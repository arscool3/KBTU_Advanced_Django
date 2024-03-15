import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app

from database import Base, engine

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_clan(test_db):
    response = client.post("/clan", json={"name": "Test Clan", "total_profit": "1000"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Clan"

    response = client.get("/clan")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Clan"


def test_create_and_get_human(test_db):
    response = client.post("/human", json={"name": "John Doe", "surname": "Doe"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"

    response = client.get("/human")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "John Doe"


def test_create_and_get_territory():
    response = client.post("/territory", json={"name": "Territory A", "address": "123 Main St"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Territory A"
    assert data["address"] == "123 Main St"

    response = client.get("/territory")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Territory A"


def test_create_and_get_business():
    # Create a business
    response = client.post("/business", json={"name": "Business A", "profit": 10000})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Business A"
    assert data["profit"] == 10000

    response = client.get("/business")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Business A"


def test_create_and_read_clan_leader():
    response = client.post("/clan_leaders/", json={"name": "Leader Name", "abilities": "Leadership"})
    assert response.status_code == 200
    data = response.json()
    assert data["abilities"] == "Leadership"

    response = client.get("/clan_leaders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Leader Name" in [leader["name"] for leader in data]


def test_create_and_read_relations():
    response = client.post("/relations/",
                           json={"name": "Relation A", "clan_1_id": 1, "clan_2_id": 2, "relation_status": "Allied"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Relation A"
    assert data["relation_status"] == "Allied"

    response = client.get("/relations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Relation A" in [relation["name"] for relation in data]
