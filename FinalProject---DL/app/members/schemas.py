from datetime import date

from app.loans.schemas import LoanResponse
from app.utils.config_schema import ConfigSchema


class BaseMember(ConfigSchema):
    full_name: str
    email: str
    phone: str
    address: str
    membership_date: date


class CreateMember(BaseMember):
    pass


class Member(BaseMember):
    id: int
    loans: list[LoanResponse]


# class MemberResponse(BaseMember):
#     id: int