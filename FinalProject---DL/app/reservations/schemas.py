from datetime import date

from app.utils.config_schema import ConfigSchema


class BaseReservation(ConfigSchema):
    reservation_date: date
    status: str


class CreateReservation(BaseReservation):
    book_id: int
    member_id: int


class Reservation(BaseReservation):
    id: int


class ReservationResponse(BaseReservation):
    id: int


class ReservationMessage(BaseReservation):
    pass

