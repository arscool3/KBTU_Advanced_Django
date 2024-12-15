from scripts.accounts.schemas import AccountResponse
from scripts.budgets.schemas import BudgetResponse
from scripts.expenses.schemas import ExpenseResponse
from utils.config_schema import ConfigSchema


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


