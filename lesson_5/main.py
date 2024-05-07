# main.py
import punq
from sqlalchemy import select
from fastapi import FastAPI
from pydantic import BaseModel
import models as db
from database import session
from schemas import Worker, CreateWorker, Company, CreateCompany, CreateJob, Job, ReturnType
from repository import WorkerRepository, AbcRepository, CompanyRepository

app = FastAPI()

class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)

def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, instance=repository(session=session))
    container.register(Dependency)
    return container

app.add_api_route("/workers", get_container(WorkerRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/companies", get_container(CompanyRepository).resolve(Dependency), methods=["GET"])

@app.post('/add_worker')
def add_worker(worker: CreateWorker) -> str:
    session.add(db.Worker(**worker.model_dump()))
    session.commit()
    session.close()
    return "Worker was added"

@app.post('/add_company')
def add_company(company: CreateCompany):
    session.add(db.Company(**company.model_dump()))
    session.commit()
    session.close()
    return "Company was added"

@app.get("/company")
def get_company():
    db_companies = session.execute(select(db.Company)).scalars().all()
    companies = []
    for db_company in db_companies:
        companies.append(Company.model_validate(db_company))
    return companies

@app.post('/add_job')
def add_job(job: CreateJob):
    session.add(db.Job(**job.model_dump()))
    session.commit()
    session.close()
    return "Job was added"

@app.get("/job")
def get_job():
    db_jobs = session.execute(select(db.Job)).scalars().all()
    jobs = []
    for db_job in db_jobs:
        jobs.append(Job.model_validate(db_job))
    return jobs


