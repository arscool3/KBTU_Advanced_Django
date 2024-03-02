from abc import abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session
import schemas
import models


class AbsRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_list(self) -> list[schemas.ReturnType]:
        raise NotImplementedError()


class UserRepository(AbsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_list(self) -> list[schemas.User]:
        db_users = self.session.execute(select(models.User)).scalars().all()
        users = []
        for user in db_users:
            users.append(user)
        return users
