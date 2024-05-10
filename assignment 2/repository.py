from abc import abstractmethod
from contextlib import contextmanager

from sqlalchemy.orm import Session

from schemas import ReturnType, Student, University, CreateUniversity, CreateStudent, CreateType
import models as db


@contextmanager
def get_db(session: Session):
    try:
        yield session
        session.commit()
    except Exception as e:
        raise
    finally:
        session.close()


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()

    def update_name(self, id: int, name: str) -> str:
        raise NotImplementedError()


class StudentRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def update_name(self, id: int, name: str) -> str:
        with get_db(self.session) as session:
            db_student = session.get(db.Student, id)
            db_student.name = name
        return "Name changed"

    def get_by_id(self, id: int) -> Student:
        with get_db(self.session) as session:
            db_student = session.get(db.Student, id)
            return Student.model_validate(db_student)


class UniversityRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> University:
        with get_db(self.session) as session:
            db_university = session.get(db.University, id)
            return University.model_validate(db_university)

    def update_name(self, id: int, name: str) -> str:
        with get_db(self.session) as session:
            db_university = session.get(db.University, id)
            db_university.name = name
        return "Name changed"
