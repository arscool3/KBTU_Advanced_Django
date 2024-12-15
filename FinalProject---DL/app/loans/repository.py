from sqlalchemy.orm import Session

from app.loans import schemas
from app.models import Loan
from app.utils.repository import BaseRepository


class LoanRepo(BaseRepository):
    model = Loan
    session = Session
    schema = schemas.Loan
