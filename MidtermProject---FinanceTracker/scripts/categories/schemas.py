from scripts.budgets.schemas import BudgetResponse
from scripts.transactions.schemas import TransactionResponse
from utils.config_schema import ConfigSchema


class BaseCategory(ConfigSchema):
    category_name: str


class Category(BaseCategory):
    id: int
    transactions: list[TransactionResponse]
    budgets: list[BudgetResponse]


class CreateCategory(BaseCategory):
    pass

