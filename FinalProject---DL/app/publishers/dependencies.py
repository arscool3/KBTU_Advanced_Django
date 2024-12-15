from fastapi import Depends
from sqlalchemy.orm import Session

from app.publishers.schemas import CreatePublisher
from app.database import get_db
from app.utils.dependencies import BaseDependency


class PublisherCreateDependency(BaseDependency):

    def __call__(self, body: CreatePublisher, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
