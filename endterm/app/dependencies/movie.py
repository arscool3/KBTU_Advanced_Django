from fastapi import Depends
from sqlalchemy.orm import Session

from app.choices.journal_choices import RequestEnum
from app.database import get_db
from app.schemas import CreateMovie
from app.services.journal import JournalWriter
from utils.dependencies import BaseDependency


class MovieCreateDependency(BaseDependency):

    def __call__(self, body: CreateMovie, session: Session = Depends(get_db)):
        self.repo.session = session
        movie_created_logger = JournalWriter()
        movie = self.repo.create(body)

        movie_created_logger.write_journal(
            data=movie,
            method='POST',
            request=RequestEnum.ADD_MOVIE.value
        )
        return movie
