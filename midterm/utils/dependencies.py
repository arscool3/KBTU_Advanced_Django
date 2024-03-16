from abc import ABC

import punq
from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database import get_db
from utils.repository import AbcRepository
from utils.schemes import CreatePost


class BaseDependency(ABC):
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, *args):
        raise NotImplementedError()


class ListDependency(BaseDependency):

    def __call__(self, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.list()


class RetrieveDependency(BaseDependency):

    def __call__(self, id: int, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.retrieve(id)


class DeleteDependency(BaseDependency):

    def __call__(self, id: int, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.delete(id)




def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())
    container.register(ListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    return container
