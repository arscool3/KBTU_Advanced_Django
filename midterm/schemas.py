from datetime import datetime

from pydantic import BaseModel


class BasicEmployer(BaseModel):
    name: str
    location: str

    class Config:
        from_attributes = True


class Employer(BasicEmployer):
    id: int


class CreateEmployer(BasicEmployer):
    pass


class BasicCandidate(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Candidate(BasicCandidate):
    id: int


class CreateCandidate(BasicCandidate):
    pass


class BasicJob(BaseModel):
    title: str
    location: str
    salary: float
    time: str
    years_of_experience: int
    employer_id: int

    class Config:
        from_attributes = True


class Job(BasicJob):
    id: int


class CreateJob(BasicJob):
    pass


class BasicSkill(BaseModel):
    title: str

    class Config:
        from_attributes = True


class Skill(BasicSkill):
    id: int


class CreateSkill(BasicSkill):
    pass


class BasicApplication(BaseModel):
    candidate_id: int
    job_id: int
    resume_id: int
    date: datetime
    status: str

    class Config:
        from_attributes = True


class Application(BasicApplication):
    id: int


class CreateApplication(BasicApplication):
    pass


class BasicResume(BaseModel):
    candidate_id: str
    location: str
    education: str
    years_of_experience: int

    class Config:
        from_attributes = True


class Resume(BasicResume):
    id: int


class CreateResume(BasicResume):
    pass
