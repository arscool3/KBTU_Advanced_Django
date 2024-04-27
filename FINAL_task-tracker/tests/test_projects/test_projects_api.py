def test_list_empty_project(test_client):
    response = test_client.get("/project")

    assert response.status_code == 200
    assert response.json() == []


def test_get_project(test_client, project):
    response = test_client.get(f"/project/{project.get('id')}")

    assert response.status_code == 200
    assert response.json()["name"] == project.get("name")


def test_create_project_error(test_client):
    response = test_client.post("/project", json={"name": "test1"})

    assert response.status_code == 422


def test_create_project(test_client):
    response = test_client.post("/project", json={"name": "test1", "description": ""})

    assert response.status_code == 200
    assert response.json()["name"] == "test1"


def test_list_non_empty_project(test_client, project):
    response = test_client.get("/project")

    assert response.status_code == 200
    assert response.json() != []
