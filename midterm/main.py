# Requirements:
# Use all topics in syllabus
# Minimum 15 api handlers (post, get) // 17
# Use DI as class, as function //  1 class, 2 function
# 6 Models, 4 relationships // 6 models, 5 relationships
# Write min 10 tests // 11 tests

from typing import Annotated
import punq
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database as db
import models
import schemas
from repository import BasicRepository, JobBasicRepository, EmployerBasicRepository, SkillBasicRepository, \
    CandidateBasicRepository, CandidateRepository, CandidateResumeRepository, CandidateApplicationRepository, \
    JobSkillRepository, JobApplicationRepository, JobRepository

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


def get_candidate_repository(repo: type[CandidateRepository]):
    def _repo_dependency(session: Session = Depends(get_db)) -> CandidateRepository:
        return repo(session)
    return _repo_dependency


def get_job_repository(repo: type[JobRepository]):
    def _repo_dependency(session: Session = Depends(get_db)) -> JobRepository:
        return repo(session)
    return _repo_dependency


def get_basic_container(repository: type[BasicRepository]) -> punq.Container:
    container = punq.Container()
    container.register(BasicRepository, repository, instance=repository(session=db.session))
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


@app.get('/jobs/skills')
def get_job_skills(id: int, repo: JobSkillRepository = Depends(get_job_repository(JobSkillRepository))):
    return repo.get_all(id=id)


@app.post('/jobs/skills')
def add_job_skills(id: int, title: str, repo: JobSkillRepository = Depends(get_job_repository(JobSkillRepository))):
    return repo.add(id=id, title=title)


@app.get('/jobs/applications')
def get_job_applications(id: int, repo: JobApplicationRepository = Depends(get_job_repository(JobApplicationRepository))):
    return repo.get_all(id=id)


@app.put('/applications/status')
def get_job_applications(id: int, title: str, repo: JobApplicationRepository = Depends(get_job_repository(JobApplicationRepository))):
    return repo.update(id=id, title=title)

