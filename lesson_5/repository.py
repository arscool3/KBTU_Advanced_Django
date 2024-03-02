from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from models import Country, President, Citizen


class BaseRepository(ABC):

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass


class CountryRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Country).filter(Country.id == id).first()


class PresidentRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(President).filter(President.id == id).first()


class CitizenRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Citizen).filter(Citizen.id == id).first()
