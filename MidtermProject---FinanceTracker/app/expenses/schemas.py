from datetime import date

from app.utils.config_schema import ConfigSchema


class BaseExpense(ConfigSchema):
    amount: float
    description: str
    expense_date: date


class Expense(BaseExpense):
    id: int


class CreateExpense(BaseExpense):
    user_id: int
    account_id: int
    category_id: int


class ExpenseResponse(BaseExpense):
    id: int