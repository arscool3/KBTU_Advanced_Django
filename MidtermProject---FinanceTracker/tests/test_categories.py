from tests.test_database import client
from tests.test_database import test_db


def test_get_categories(test_db):
    response = client.get("/category/get_categories")
    assert response.json() == []


def test_add_category(test_db):
    response = client.post("/category/create_category", json={
        'category_name': 'category',
        'transactions': [],
        'budgets': []
    })
    assert response.status_code == 200

    response = client.get("/category/get_categories")
    assert response.json() == [
        {
            'id': 1,
            'category_name': 'category',
            'transactions': [],
            'budgets': []
        }
    ]
