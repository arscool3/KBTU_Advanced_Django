# Job site
# job -> title, salary, time, experience, employer(many to one)(1), skills (many to many)(2)
# employer -> name, location, jobs (one to many)(1)
# candidate -> name, age, applications(one to many)(3), resumes(one to many)(4)
# skill -> title, jobs(2), applications(many to many)(5)
# application -> candidate_id, job_id, date, status, candidate(many to one)(3)
# resume -> candidates_id, skills(many to many)(5), candidate(many to one)(4), experience, education

# try yield finally

# Requirements:
# Use all topics in syllabus
# Minimum 15 api handlers (post, get) // 17
# Use DI as class, as function // 0 - callable and with methods
# 6 Models, 4 relationships // 6 models, 5 relationships
# Write min 10 tests // 0

from typing import Annotated
import punq
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database as db
import models
import schemas
from repository import BasicRepository, JobBasicRepository, EmployerBasicRepository, SkillBasicRepository, \
    CandidateBasicRepository, CandidateRepository, CandidateResumeRepository, CandidateApplicationRepository

app = FastAPI()


class BasicDependency:
    def __init__(self, repo: BasicRepository):
        self.repo = repo

    def __call__(self):
        return self.repo

    def get_all(self) -> list[schemas.ReturnType]:
        return self.repo.get_all()

    def add(self, data: schemas.CreateType):
        return self.repo.add(data)


def get_db():
    try:
        yield db.session
        db.session.commit()
    except:
        raise NotImplementedError()
    finally:
        db.session.close()


def get_candidate_repository(repo: type[BasicRepository]):
    def _repo_dependency(session: Session = Depends(get_db)) -> BasicRepository:
        return repo(session)
    return _repo_dependency


def get_basic_container(repository: type[BasicRepository]) -> punq.Container:
    container = punq.Container()
    container.register(BasicRepository, repository, instance=repository(session=db.session))
    container.register(BasicDependency)
    return container


def get_candidate_container(repository: type[CandidateRepository]) -> punq.Container:
    container = punq.Container()
    container.register(CandidateRepository, repository, instance=repository(session=db.session))
    container.register(BasicDependency)
    return container


@app.get('/employers')
def get_employers(employers: Annotated[list[schemas.Employer], Depends(get_basic_container(EmployerBasicRepository).resolve(BasicDependency).get_all)]):
    return 'No employers' if employers is None else employers


@app.post('/employers')
def add_employer(employer: schemas.CreateEmployer, repo: EmployerBasicRepository = Depends(get_basic_container(EmployerBasicRepository).resolve(BasicDependency))):
    return 'Try again' if employer is None else repo.add(data=employer)


@app.get('/jobs')
def get_jobs(jobs: Annotated[list[schemas.Job], Depends(get_basic_container(JobBasicRepository).resolve(BasicDependency).get_all)]):
    return 'No jobs' if jobs is None else jobs


@app.post('/jobs')
def add_employer(job: schemas.CreateJob, repo: JobBasicRepository = Depends(get_basic_container(JobBasicRepository).resolve(BasicDependency))):
    return 'Try again' if job is None else repo.add(data=job)


@app.post('/candidates')
def add_employer(candidate: schemas.CreateCandidate, repo: CandidateBasicRepository = Depends(get_basic_container(CandidateBasicRepository).resolve(BasicDependency))):
    return 'Try again' if candidate is None else repo.add(data=candidate)


@app.get('/candidates')
def get_candidate_by_id(id: int, repo: CandidateBasicRepository = Depends(get_basic_container(CandidateBasicRepository).resolve(BasicDependency))):
    return 'Try again' if id is None else repo.get_by_id(id=id)


@app.get('/skills')
def get_skills(skills: Annotated[list[schemas.Skill], Depends(get_basic_container(SkillBasicRepository).resolve(BasicDependency).get_all)]):
    return 'No skills' if skills is None else skills


@app.post('/skills')
def add_skill(skill: schemas.CreateSkill, repo: SkillBasicRepository = Depends(get_basic_container(SkillBasicRepository).resolve(BasicDependency))):
    return 'Try again' if skill is None else repo.add(data=skill)


@app.get('/skills/{title}')
def get_skills(title: str, repo: SkillBasicRepository = Depends(get_basic_container(SkillBasicRepository).resolve(BasicDependency))):
    return repo.get_by_title(title=title)


@app.post('/candidates/resumes')
def add_resume_to_candidate(data: schemas.CreateResume, repo: CandidateResumeRepository = Depends(get_candidate_repository(CandidateResumeRepository))):
    return repo.add(data=data)


@app.get('/candidates/resumes')
def get_candidate_resumes(id: int, repo: CandidateResumeRepository = Depends(get_candidate_repository(CandidateResumeRepository))):
    return repo.get_all(id=id)


@app.post('/candidates/applications')
def add_application_to_candidate(data: schemas.CreateApplication, repo: CandidateApplicationRepository = Depends(get_candidate_repository(CandidateApplicationRepository))):
    return repo.add(data=data)


@app.get('/candidates/applications')
def get_candidate_resumes(id: int, repo: CandidateApplicationRepository = Depends(get_candidate_repository(CandidateApplicationRepository))):
    return repo.get_all(id=id)


@app.post('/jobs/skills')
def add_skill_to_job(job_id: int, skill_title: str):
    db_job = db.session.get(models.Job, job_id)
    db_skill = db.session.query(models.Skill).filter(models.Skill.title == skill_title).first()
    db_skill.jobs.append(db_job)
    db_job.skills.append(db_skill)
    job = schemas.Job.model_validate(db_job)
    db.session.commit()
    db.session.close()
    return f"{skill_title} was added to candidate: {job.title}"


@app.get('/jobs/skills')
def get_job_skills(job_id: int):
    db_job = db.session.get(models.Job, job_id)
    job = schemas.Job.model_validate(db_job)
    db_skills = db_job.skills
    skills = [schemas.Skill.model_validate(skill) for skill in db_skills]
    return f"Skills that is {job.title} required: {skills}"


@app.get('/jobs/applications')
def get_job_applications(job_id: int):
    db_job = db.session.get(models.Job, job_id)
    db_applications = db_job.applications
    applications = [schemas.Application.model_validate(application) for application in db_applications]
    return applications


@app.put('/applications')
def get_job_applications(application_id: int, status: str):
    db_applications = db.session.get(models.Application, application_id)
    setattr(db_applications, 'status', status)
    application = schemas.Application.model_validate(db_applications)
    db.session.commit()
    db.session.close()
    return application
