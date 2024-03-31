from app.transactions.schemas import TransactionResponse
from app.utils.config_schema import ConfigSchema


class BaseAccount(ConfigSchema):
    account_name: str
    account_type: str


class Account(BaseAccount):
    id: int
    transactions: list[TransactionResponse]


class CreateAccount(BaseAccount):
    user_id: int


class AccountResponse(BaseAccount):
    id: int
