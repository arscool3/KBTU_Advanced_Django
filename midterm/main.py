from datetime import date
import punq
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

import database as db
from database import session
from repository import AbcRepository, UserRepository, ProjectRepository, TaskStatusRepository, \
    TaskAssignmentRepository, ReportRepository
from schemas import ProjectSchema, User, TaskSchema, TaskStatusSchema, TaskAssignment, Report, CreateUser, \
    CreateProject, CreateTask, CreateTaskAssignment, CreateTaskStatus, CreateReport, UpdateUser, UpdateProject, \
    UpdateTask, UpdateReport

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> (User | ProjectSchema | TaskSchema | TaskStatusSchema | Report | TaskAssignment):
        return self.repo.get_by_id(id)


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


@app.post('/users')
def add_user(user: CreateUser, session: Session = Depends(get_db)) -> str:
    session.add(db.User(**user.model_dump()))
    return user.name


@app.get("/users")
def get_users(session: Session = Depends(get_db)) -> list[User]:
    db_users = session.execute(select(db.User)).scalars().all()
    user = [User.model_validate(db_user) for db_user in db_users]
    return user


app.add_api_route("/get_user_by_id", get_container(UserRepository).resolve(Dependency), methods=["GET"])


@app.post('/projects')
def add_projects(project: CreateProject, user_id: int, session: Session = Depends(get_db)) -> str:
    db_project = db.Project(
        name=project.name,
        created_at=date.today(),
        user_id=user_id
    )
    session.add(db_project)
    session.commit()
    return db_project.name


@app.get("/projects")
def get_projects(session: Session = Depends(get_db)) -> list[ProjectSchema]:
    db_projects = session.execute(select(db.Project)).scalars().all()
    projects = []

    for db_project in db_projects:
        project_data = db_project.__dict__
        project_data['tasks'] = []
        projects.append(ProjectSchema(**project_data))
    return projects


app.add_api_route("/get_project_by_id", get_container(ProjectRepository).resolve(Dependency), methods=["GET"])


@app.post('/tasks')
def add_tasks(task: CreateTask, project_name: str, user_name: str, session: Session = Depends(get_db)) -> str:
    project = session.query(db.Project).filter(db.Project.name == project_name).first()
    if project is None:
        return "Project not found"

    user = session.query(db.User).filter(db.User.name == user_name).first()
    if user is None:
        return "User not found"

    new_task = db.Task(name=task.name, project_id=project.id, user_id=user.id)
    session.add(new_task)
    session.commit()
    return task.name


def db_to_dict(task: db.Task):
    return {
        "id": task.id,
        "name": task.name,
        "project_id": task.project_id,
        "user_id": task.user_id,
    }


@app.get('/tasks')
def get_tasks(session: Session = Depends(get_db)):
    tasks = session.query(db.Task).all()
    return [db_to_dict(task) for task in tasks]


@app.post('/task_assignments')
def add_assignment(ass: CreateTaskAssignment, session: Session = Depends(get_db)) -> str:
    session.add(db.TaskAssignment(**ass.model_dump()))
    return ass.name


@app.get("/task_assignments")
def get_assignments(session: Session = Depends(get_db)) -> list[TaskAssignment]:
    db_asses = session.execute(select(db.TaskAssignment)).scalars().all()
    ass = [TaskAssignment.model_validate(db_ass) for db_ass in db_asses]
    return ass


app.add_api_route("/get_assignment_by_id", get_container(TaskAssignmentRepository).resolve(Dependency), methods=["GET"])


@app.post('/task_statuses')
def add_status(task_name: str, status: CreateTaskStatus, session: Session = Depends(get_db)) -> str:
    task = session.query(db.Task).filter(db.Task.name == task_name).first()
    if task is None:
        return "Task not found"

    new_status = db.TaskStatus(name=status.name, task_id=task.id)
    session.add(new_status)
    session.commit()
    return status.name


@app.get("/task_statuses")
def get_task_statuses(session: Session = Depends(get_db)):
    task_statuses = session.query(db.TaskStatus).all()
    return [{
            "id": status.id,
            "task_id": status.task_id,
        }
        for status in task_statuses
    ]


app.add_api_route("/get_status_by_id", get_container(TaskStatusRepository).resolve(Dependency), methods=["GET"])


@app.post("/reports")
def add_report(report: CreateReport, session: Session = Depends(get_db)) -> str:
    session.add(db.Report(**report.model_dump()))
    return report.name


@app.get("/reports")
def get_reports(session: Session = Depends(get_db)) -> list[Report]:
    db_reports = session.execute(select(db.Report)).scalars().all()
    reports = [Report.model_validate(db_report) for db_report in db_reports]
    return reports


app.add_api_route("/get_report_dy_id", get_container(ReportRepository).resolve(Dependency), methods=["GET"])


@app.put("/user")
def update_user(user_id: int, user: UpdateUser, session: Session = Depends(get_db)) -> str:
    db_user = session.query(db.User).filter(db.User.id == user_id).first()
    if not user:
        return "User not found"

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.commit()
    return user.name


@app.put("/project")
def update_project(project_id: int, project: UpdateProject, session: Session = Depends(get_db)) -> str:
    db_project = session.query(db.Project).filter(db.Project.id == project_id).first()
    if not db_project:
        return "Project not found"

    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)

    session.commit()
    return project.name


@app.put("/task")
def update_task(task_id: int, task: UpdateTask, session: Session = Depends(get_db)) -> str:
    db_task = session.query(db.Task).filter(db.Task.id == task_id).first()
    if not db_task:
        return "Task not found"

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.commit()
    return task.name


@app.put("/report")
def update_report(report_id: int, report: UpdateReport, session: Session = Depends(get_db)) -> str:
    db_report = session.query(db.Report).filter(db.Report.id == report_id).first()
    if not db_report:
        return "Report not found"

    report_data = report.dict(exclude_unset=True)
    for key, value in report_data.items():
        setattr(db_report, key, value)

    session.commit()
    return report.name
