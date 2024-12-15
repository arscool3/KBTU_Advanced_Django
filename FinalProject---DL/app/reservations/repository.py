from sqlalchemy.orm import Session

from app.models import Reservation
from app.reservations import schemas
from app.utils.repository import BaseRepository


class ReservationRepo(BaseRepository):
    model = Reservation
    session = Session
    schema = schemas.Reservation
