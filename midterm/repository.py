from abc import abstractmethod
from sqlalchemy.orm import Session

import schemas
from schemas import ReturnType, CreateType
import models
from sqlalchemy import select
import database as db

# job -> get all, post, job_applications, job_candidates
# employer -> get all, post
# skill -> get all, post, by title
# candidate -> candidate_resumes, candidate_applications, post, by id
# application ->
# resume ->

class BasicRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_all(self) -> list[ReturnType]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, data: CreateType) -> str:
        raise NotImplementedError()


class JobBasicRepository(BasicRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[schemas.Job]:
        db_jobs = self.session.execute(select(models.Job)).scalars().all()
        jobs = [schemas.Job.model_validate(job) for job in db_jobs]
        return jobs

    # there's some error -> create type
    def add(self, data: schemas.CreateJob) -> str:
        self.session.add(models.Job(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return f"{data.title} was added"

