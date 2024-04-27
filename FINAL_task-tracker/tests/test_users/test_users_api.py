import pytest


def test_list_users_empty_list(test_client):
    response = test_client.get("/user/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(test_client, project):
    response = test_client.post("/user/", json={
      "first_name": "string",
      "last_name": "string",
      "email": "user@example.com",
      "project_id": project["id"],
    })

    assert response.status_code == 200
    assert response.json()["first_name"] == "string"
    assert response.json()["last_name"] == "string"


def test_create_user_error(test_client, project):
    response = test_client.post("/user/", json={
      "last_name": "string",
      "email": "user@example.com",
      "project_id": project["id"],
    })

    assert response.status_code == 422


def test_users_list(test_client, user):
    response = test_client.get("/user/")

    assert response.status_code == 200
    assert response.json() != []
    assert len(response.json()) == 1


def test_get_user(test_client, user):
    response = test_client.get(f"/user/{user['id']}/")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["email"] == user["email"]
    assert response.json()["first_name"] == user["first_name"]
    assert response.json()["last_name"] == user["last_name"]
