from accounts.schemas import AccountResponse
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
    # budgets: list[Budget]
    # expenses: list[Expense]


