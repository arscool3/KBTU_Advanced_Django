from app.accounts.schemas import AccountResponse
from app.budgets.schemas import BudgetResponse
from app.expenses.schemas import ExpenseResponse
from app.utils.config_schema import ConfigSchema


class BaseUser(ConfigSchema):
    username: str
    email: str
    password: str


class CreateUser(BaseUser):
    pass


class User(BaseUser):
    id: int
    accounts: list[AccountResponse]
    budgets: list[BudgetResponse]
    expenses: list[ExpenseResponse]


