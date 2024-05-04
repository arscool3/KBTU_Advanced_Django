from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateGenre, Director
from app.services.journal import JournalWriter
from utils.dependencies import BaseDependency
from ..choices.journal_choices import RequestEnum


class DirectorCreateDependency(BaseDependency):

    def __call__(self, body: Director, session: Session = Depends(get_db)):
        self.repo.session = session
        director_created_logger = JournalWriter()

        director = self.repo.create(body)
        director_created_logger.write_journal(
            data=director,
            method='POST',
            request=RequestEnum.ADD_DIRECTOR.value,
        )
        return director
