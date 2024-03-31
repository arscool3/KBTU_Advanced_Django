from abc import ABC

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.repository import AbcRepository


class BaseDependency(ABC):
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class GetListDependency(BaseDependency):
    def __call__(self, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.get_list()


class RetrieveDependency(BaseDependency):

    def __call__(self, id: int, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.retrieve(id)


class DeleteDependency(BaseDependency):

    def __call__(self, id: int, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.delete(id)
