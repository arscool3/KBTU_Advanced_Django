from datetime import date

from app.utils.config_schema import ConfigSchema


class BaseLoan(ConfigSchema):
    loan_date: date
    status: str


class Loan(BaseLoan):
    id: int


class CreateLoan(BaseLoan):
    book_id: int
    member_id: int


class LoanResponse(BaseLoan):
    id: int
