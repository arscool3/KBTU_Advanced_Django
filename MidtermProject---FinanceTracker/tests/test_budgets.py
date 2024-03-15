from datetime import date

from tests.test_categories import test_add_category
from tests.test_database import client
from tests.test_users import test_add_user
from tests.test_database import test_db


def test_get_budgets(test_db):
    response = client.get("/budget/get_budgets")
    assert response.json() == []


def test_add_budget(test_db):
    test_add_user(test_db)
    test_add_category(test_db)

    response = client.post("/budget/create_budget", json={
        'user_id': 1,
        'category_id': 1,
        'amount': 500.0,
        'added_date': f'{date.today()}'
    })
    assert response.status_code == 200
