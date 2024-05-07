from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
from schemas import Worker, Job, Company, ReturnType


class AbcRepository:

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class WorkerRepository(AbcRepository):
    
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Worker:
        db_worker = self._session.get(db.Worker, id)
        return Worker.model_validate(db_worker)


class CompanyRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Company:
        db_company = self.session.get(db.Company, id)
        return Company.model_validate(db_company)
