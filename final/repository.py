from abc import abstractmethod

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
from schemas import User, Event, ReturnType

class Repository:

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class UserRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> User:
        db_user = self._session.get(db.User, id)
        return User.model_validate(db_user)

    def get_all(self) -> list[User]:
        db_users = self._session.execute(select(db.User)).scalars().all()
        users = []
        for db_user in db_users:
            users.append(User.model_validate(db_user))
        return users


class EventRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Event:
        db_event = self._session.get(db.Event, id)
        return Event.model_validate(db_event)

    def get_all(self) -> list[Event]:
        db_events = self._session.execute(select(db.Event)).scalars().all()
        events = []
        for db_event in db_events:
            events.append(Event.model_validate(db_event))
        return events