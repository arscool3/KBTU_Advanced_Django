import datetime
from typing import List

from pydantic import BaseModel, Field


class BasingModel(BaseModel):
    class Config:
        from_attributes = True


class User(BasingModel):
    id: int
    username: str


class CreateUser(BasingModel):
    username: str


class UserComplaint(BasingModel):
    id: int
    user_id: int
    project_id: int
    description: str


class CreateUserComplaint(BasingModel):
    user_id: int
    project_id: int = 0
    description: str


class Organization(BasingModel):
    id: int
    name: str
    num_of_finished_projects: int


class CreateOrganization(BasingModel):
    name: str


class TbOrganization(BasingModel):
    name: str
    num_of_finished_projects: int = 0


class Investor(BasingModel):
    id: int
    name: str


class CreateInvestor(BasingModel):
    name: str


class Project(BasingModel):
    id: int
    organization_id: int
    investor_id: int
    initial_budget: float
    current_budget: float
    promised_end_date: datetime.datetime
    is_finished: bool


class CreateProject(BasingModel):
    organization_id: int
    investor_id: int
    initial_budget: float
    current_budget: float
    promised_end_date: datetime.datetime
    start_date: datetime.datetime = datetime.datetime.now()
    is_finished: bool = False


class State(BasingModel):
    id: int
    project_id: int
    last_total_spent_money: float
    report: str
    future_plan: str
    created_at: datetime.datetime


class CreateState(BasingModel):
    project_id: int = 0
    last_total_spent_money: float
    report: str
    future_plan: str
    created_at: datetime.datetime = datetime.datetime.now()


class Log(BasingModel):
    id: int
    created_at: datetime.datetime = datetime.datetime.now()
    data: str
    method: str
    request: str


class CreateLog(BasingModel):
    data: str
    method: str
    request: str
