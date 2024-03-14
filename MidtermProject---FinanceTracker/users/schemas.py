from models import Account, Budget, Expense
from utils.config_schema import ConfigSchema


class BaseUser(ConfigSchema):
    username: str
    email: str
    password: str


class User(BaseUser):
    id: int
    accounts: list[Account]
    budgets: list[Budget]
    expenses: list[Expense]


class CreateUser(BaseUser):
    pass
