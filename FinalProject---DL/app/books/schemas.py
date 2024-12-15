from app.loans.schemas import LoanResponse
from app.reservations.schemas import ReservationResponse
from app.utils.config_schema import ConfigSchema


class BaseBook(ConfigSchema):
    title: str
    year: int
    genre: str
    summary: str
    available_copies: int


class Book(BaseBook):
    id: int
    loans: list[LoanResponse]
    reservations: list[ReservationResponse]


class CreateBook(BaseBook):
    author_id: int
    publisher_id: int


class BookResponse(BaseBook):
    id: int
