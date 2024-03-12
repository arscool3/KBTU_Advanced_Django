from fastapi.testclient import TestClient

from igscraper.stalku.main import app

client = TestClient(app)


def test_create_target():
    response = client.get("/1234567890")
    assert response.status_code == 201
    assert response.json() == {"uid": "1234567890"}


def test_read_target():
    client.get("/1234567890")
    response = client.get("/1234567890")
    assert response.status_code == 200
    assert response.json()["uid"] == "1234567890"


def test_read_targets():
    client.get("/1234567890")
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_target():
    client.get("/1234567890")
    response = client.put("/1234567890", json={"uid": "0987654321"})
    assert response.status_code == 200
    assert response.json()["uid"] == "0987654321"


def test_delete_target():
    client.get("/1234567890")
    response = client.delete("/1234567890")
    assert response.status_code == 200
    assert response.json()["uid"] == "1234567890"


def test_delete_all_targets():
    client.get("/1234567890")
    response = client.delete("/")
    assert response.status_code == 200
    assert response.json()["message"] == "All targets deleted successfully."


def test_fetch_target_followers():
    response = client.get("/1234567890/followers/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_fetch_target_followings():
    response = client.get("/1234567890/following/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_fetch_target_username():
    response = client.get("/1234567890/to_username")
    assert response.status_code == 200
    assert "username" in response.json()


def test_fetch_target_uid():
    response = client.get("/testuser/to_uid")
    assert response.status_code == 200
    assert "uid" in response.json()
