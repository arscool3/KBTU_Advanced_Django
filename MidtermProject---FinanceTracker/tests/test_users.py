from tests.test_database import client
from tests.test_database import test_db


def test_get_users(test_db):
    response = client.get("/user/get_users")
    assert response.json() == []


def test_add_user(test_db):
    response = client.post("/user/create_user", json={
        'username': 'Bakdaulet',
        'email': 'bakdaulet@gmail.com',
        'password': '123123123'
    })
    assert response.status_code == 200

    response = client.get("/user/get_users")
    assert response.json() == [
        {
            'id': 1,
            'username': 'Bakdaulet',
            'email': 'bakdaulet@gmail.com',
            'password': '123123123',
            'accounts': [],
            'budgets': [],
            'expenses': []
        }
    ]