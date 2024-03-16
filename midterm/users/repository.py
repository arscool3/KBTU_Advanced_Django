from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.repository import AbcRepository
from utils.schemes import User
import utils.models as db


class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def retrieve(self, user_id: int):
        return self.session.execute(select(db.User).where(db.User.id == user_id)).scalars().first()

    def create(self, user: User) -> str:
        pass

    def delete(self, user_id: int):
        pass

    def list(self) -> List[User]:
        pass
