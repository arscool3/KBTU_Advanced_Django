from typing import List

from fastapi import FastAPI, Depends, HTTPException

from dramatiq_worker import change_budget, project_fatality
from producer import produce_log
import models as db
from schemas import CreateUser, User, UserComplaint, CreateUserComplaint, Organization, CreateOrganization, Investor, \
    CreateInvestor, Project, CreateProject, State, CreateState, TbOrganization
from database import get_db, Base, engine

app = FastAPI()


@app.get("/")
def welcome() -> str:
    return "Welcome to"


@app.post("/users")
def create_user(user: CreateUser) -> str:
    with get_db() as session:
        session.add(db.User(**user.model_dump()))

    produce_log({
        "data": "Users created",
        "method": 'POST',
        "request": "create_user",
    })
    return "User created"


@app.get("/users")
def get_users():
    with get_db() as session:
        db_users = session.query(db.User).all()
        users = []
        for db_user in db_users:
            users.append(User.model_validate(db_user))

        produce_log({
            "data": "Users retrieved",
            "method": 'GET',
            "request": "get_users",
        })
        return users


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int) -> User:
    with get_db() as session:
        db_user = session.query(db.User).filter(db.User.id == user_id).first()

        produce_log({
            "data": "User by id retrieved",
            "method": 'GET',
            "request": "get_user_by_id",
        })
        return User.model_validate(db_user)


@app.get("/organizations")
def get_organizations() -> List[Organization]:
    with get_db() as session:
        db_organizations = session.query(db.Organization).all()
        organizations = []
        for db_organization in db_organizations:
            organizations.append(Organization.model_validate(db_organization))
        produce_log({
            "data": "Organizations retrieved",
            "method": 'GET',
            "request": "get_organizations",
        })
        return organizations


@app.post("/organizations")
def create_organization(organization: CreateOrganization) -> str:
    with get_db() as session:
        org = TbOrganization(**organization.model_dump())
        print(org)
        session.add(db.Organization(**org.model_dump()))

    produce_log({
        "data": "Organization created",
        "method": 'POST',
        "request": "create_organization",
    })
    return "Organization created"


@app.get("/investors")
def get_investors() -> List[Investor]:
    with get_db() as session:
        db_investors = session.query(db.Investor).all()
        investors = []
        for db_investor in db_investors:
            investors.append(Investor.model_validate(db_investor))

        produce_log({
            "data": "Investors retrieved",
            "method": 'GET',
            "request": "get_investors",
        })
        return investors


@app.post("/investors")
def create_investor(investor: CreateInvestor) -> str:
    with get_db() as session:
        session.add(db.Investor(**investor.model_dump()))

    produce_log({
        "data": "Investor created",
        "method": 'POST',
        "request": "create_investor",
    })
    return "Investor created"


@app.get("/projects")
def get_projects() -> List[Project]:
    with get_db() as session:
        db_projects = session.query(db.Project).all()
        projects = []
        for db_project in db_projects:
            projects.append(Project.model_validate(db_project))
        produce_log({
            "data": "Projects retrieved",
            "method": 'GET',
            "request": "get_projects",
        })
        return projects


@app.post("/projects")
def create_project(project: CreateProject) -> str:
    with get_db() as session:
        session.add(db.Project(**project.model_dump()))
    produce_log({
        "data": "Project created",
        "method": 'POST',
        "request": "create_project",
    })
    return "Project created"


def project_exist(project_id: int):
    with get_db() as session:
        db_project = session.query(db.Project).filter(db.Project.id == project_id).first()
        if not db_project:
            return 0, False
        return project_id, True


@app.get("/projects/{project_id}/finish")
def finish_project(project_id_set=Depends(project_exist)):
    project_id = project_id_set[0]
    exist = project_id_set[1]
    if not exist:
        raise HTTPException(status_code=404, detail="Project does not exist")

    project_fatality.send(project_id=project_id)
    produce_log({
        "data": "Project finished",
        "method": 'GET',
        "request": "finish_project",
    })
    return "Project finished"


@app.get("/projects/{project_id}/states")
def get_states(project_id_set=Depends(project_exist)) -> List[State]:
    project_id = project_id_set[0]
    exist = project_id_set[1]
    if not exist:
        raise HTTPException(status_code=404, detail="Project does not exist")
    with get_db() as session:
        db_states = session.query(db.State).filter(db.State.project_id == project_id).all()
        states = []
        for db_state in db_states:
            states.append(State.model_validate(db_state))
        produce_log({
            "data": "States retrieved",
            "method": 'GET',
            "request": "get_states",
        })
        return states


@app.post("/projects/{project_id}/states")
def create_state(project_id: int, state: CreateState) -> str:
    with get_db() as session:
        state.project_id = project_id
        session.add(db.State(**state.model_dump()))
    change_budget.send(amount=state.last_total_spent_money, project_id=state.project_id)
    produce_log({
        "data": "State created",
        "method": 'POST',
        "request": "create_state",
    })
    return "State created"


@app.get("/projects/{project_id}/complaints")
def get_complaints(project_id: int) -> List[UserComplaint]:
    with get_db() as session:
        db_complaints = session.query(db.UserComplaint).filter(db.UserComplaint.project_id == project_id).all()
        complaints = []
        for db_complaint in db_complaints:
            complaints.append(UserComplaint.model_validate(db_complaint))

        produce_log({
            "data": "Complaints retrieved",
            "method": 'GET',
            "request": "get_complaints",
        })
        return complaints


@app.post("/projects/{project_id}/complaints")
def create_complaint(project_id: int, complaint: CreateUserComplaint) -> str:
    with get_db() as session:
        complaint.project_id = project_id
        session.add(db.UserComplaint(**complaint.model_dump()))
    produce_log({
        "data": "Complaint created",
        "method": 'POST',
        "request": "create_complaint",
    })
    return "User complaint created"


Base.metadata.create_all(bind=engine)
