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
    def add(self, data: CreateType) -> CreateType:
        raise NotImplementedError()


class JobBasicRepository(BasicRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[schemas.Job]:
        db_jobs = self.session.execute(select(models.Job)).scalars().all()
        jobs = [schemas.Job.model_validate(job) for job in db_jobs]
        return jobs

    # there's some error -> create type
    def add(self, data: schemas.CreateJob) -> schemas.CreateJob:
        self.session.add(models.Job(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return data


class EmployerBasicRepository(BasicRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[schemas.Employer]:
        db_employers = self.session.execute(select(models.Employer)).scalars().all()
        employers = [schemas.Employer.model_validate(employer) for employer in db_employers]
        return employers

    def add(self, data: schemas.CreateEmployer) -> schemas.CreateEmployer:
        self.session.add(models.Employer(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return data


class SkillBasicRepository(BasicRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[schemas.Skill]:
        db_skills = self.session.execute(select(models.Skill)).scalars().all()
        skills = [schemas.Skill.model_validate(skill) for skill in db_skills]
        return skills

    def add(self, data: schemas.CreateSkill) -> schemas.CreateSkill:
        self.session.add(models.Skill(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return data

    def get_by_title(self, title: str):
        db_skill = self.session.query(models.Skill).filter(models.Skill.title == title).first()
        if db_skill is None:
            return None
        skill = schemas.Skill.model_validate(db_skill)
        return skill


class CandidateBasicRepository(BasicRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[schemas.Skill]:
        pass

    def add(self, data: schemas.CreateCandidate) -> schemas.CreateCandidate:
        self.session.add(models.Candidate(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return data

    def get_by_id(self, id: int):
        db_candidate = self.session.get(models.Candidate, id)
        if db_candidate is None:
            return None
        candidate = schemas.Candidate.model_validate(db_candidate)
        return candidate


class CandidateRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_all(self, id: int) -> list[ReturnType]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, data: CreateType) -> CreateType:
        raise NotImplementedError()


class CandidateResumeRepository(CandidateRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, id: int):
        db_candidate = self.session.get(models.Candidate, id)
        candidate = schemas.Candidate.model_validate(db_candidate)
        db_resumes = db_candidate.resumes
        resumes = [schemas.Resume.model_validate(resume) for resume in db_resumes]
        return f"{candidate.name}'s resumes: {resumes}"

    def add(self, data: schemas.CreateResume):
        db_candidate = self.session.get(models.Candidate, data.candidate_id)
        candidate = schemas.Candidate.model_validate(db_candidate)
        self.session.add(models.Resume(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return f"New resume was added to candidate: {candidate.name}"


class CandidateApplicationRepository(CandidateRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, id: int):
        db_candidate = self.session.get(models.Candidate, id)
        candidate = schemas.Candidate.model_validate(db_candidate)
        db_applications = db_candidate.applications
        applications = [schemas.Application.model_validate(application) for application in db_applications]
        return f"Jobs that is {candidate.name} applied: {applications}"

    def add(self, data: schemas.CreateApplication):
        db_candidate = self.session.get(models.Candidate, data.candidate_id)
        db_job = self.session.get(models.Job, data.job_id)
        db_resume = self.session.get(models.Resume, data.resume_id)

        candidate = schemas.Candidate.model_validate(db_candidate)
        job = schemas.Job.model_validate(db_job)
        resume = schemas.Resume.model_validate(db_resume)

        if db_resume.candidate_id != data.candidate_id:
            return "Such resume doesn't exists"
        self.session.add(models.Application(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return f"{candidate.name} applied to the job: {job.title} with resume {resume.title}"


class JobRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_all(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def add(self, id: int, title: str):
        raise NotImplementedError()

    @abstractmethod
    def update(self, id: int, title: str):
        raise NotImplementedError()


class JobSkillRepository(JobRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, id: int):
        db_job = self.session.get(models.Job, id)
        job = schemas.Job.model_validate(db_job)
        db_skills = db_job.skills
        skills = [schemas.Skill.model_validate(skill) for skill in db_skills]
        return f"Skills that is {job.title} required: {skills}"

    def add(self, id: int, title: str):
        db_job = self.session.get(models.Job, id)
        db_skill = self.session.query(models.Skill).filter(models.Skill.title == title).first()
        db_skill.jobs.append(db_job)
        db_job.skills.append(db_skill)
        job = schemas.Job.model_validate(db_job)
        self.session.commit()
        self.session.close()
        return f"{title} was added to candidate: {job.title}"

    def update(self, id: int, title: str):
        pass


class JobApplicationRepository(JobRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, id: int):
        db_job = db.session.get(models.Job, id)
        db_applications = db_job.applications
        applications = [schemas.Application.model_validate(application) for application in db_applications]
        return applications

    def add(self, id: int, title: str):
        pass

    def update(self, id: int, title: str):
        db_applications = db.session.get(models.Application, id)
        setattr(db_applications, 'status', title)
        application = schemas.Application.model_validate(db_applications)
        db.session.commit()
        db.session.close()
        return application
