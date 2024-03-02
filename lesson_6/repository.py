from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from models import Movie, Director, Genre, Studio


class BaseRepository(ABC):

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass


class MovieRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Movie).filter(Movie.id == id).first()


class DirectorRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Director).filter(Director.id == id).first()


class GenreRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Genre).filter(Genre.id == id).first()


class StudioRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int):
        return self.session.query(Studio).filter(Studio.id == id).first()
