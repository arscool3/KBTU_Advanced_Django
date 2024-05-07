from pydantic import BaseModel
from datetime import date


class BaseJob(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True

class Job(BaseJob):
    id: int


class CreateJob(BaseJob):
    pass

class BaseCompany(BaseModel):
    name: str
    industry: str
    established_date: date

    class Config:
        from_attributes = True

class CreateCompany(BaseCompany):
    pass

class Company(BaseCompany):
    id: int

class BaseWorker(BaseModel):
    name: str
    age: int
    
    class Config:
        from_attributes = True

class CreateWorker(BaseWorker):
    job_id: int

class Worker(BaseWorker):
    id: int
    job: Job


ReturnType = Worker | Company | Job
