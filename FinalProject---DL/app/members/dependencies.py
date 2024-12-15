from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.members.schemas import CreateMember
from app.utils.dependencies import BaseDependency


class MemberCreateDependency(BaseDependency):

    def __call__(self, body: CreateMember, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
