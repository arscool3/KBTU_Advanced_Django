from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.reservations.schemas import CreateReservation
from app.utils.dependencies import BaseDependency


class ReservationCreateDependency(BaseDependency):

    def __call__(self, body: CreateReservation, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
