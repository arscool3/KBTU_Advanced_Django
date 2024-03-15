from datetime import date

from utils.config_schema import ConfigSchema


class BaseBudget(ConfigSchema):
    amount: float
    added_date: date


class Budget(BaseBudget):
    id: int


class CreateBudget(BaseBudget):
    user_id: int
    category_id: int


class BudgetResponse(BaseBudget):
    id: int