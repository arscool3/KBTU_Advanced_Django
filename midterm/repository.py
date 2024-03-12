from abc import abstractmethod

from sqlalchemy.orm import Session, joinedload

import database as db
from schemas import (User, ProjectSchema, TaskSchema, TaskStatusSchema, Report, TaskAssignment)


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> User | ProjectSchema | TaskSchema | TaskStatusSchema | Report | TaskAssignment:
        raise NotImplementedError()



class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> User:
        db_user = self._session.get(db.User, id)
        return User.model_validate(db_user)


class ProjectRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> ProjectSchema:
        db_project = self._session.query(db.Project).filter(db.Project.id == id).options(
            joinedload(db.Project.tasks)).first()
        return ProjectSchema.model_validate(db_project)


class TaskRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> TaskSchema:
        db_task = self._session.query(db.Task).filter(db.Task.id == id).first()
        return TaskSchema.model_validate(db_task)


class TaskAssignmentRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> TaskAssignment:
        db_task_assignment = self._session.get(db.TaskAssignment, id)
        return TaskAssignment.model_validate(db_task_assignment)


class ReportRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Report:
        db_report = self._session.get(db.Report, id)
        return Report.model_validate(db_report)


class TaskStatusRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> TaskStatusSchema:
        db_task_status = self._session.get(db.TaskStatus, id)
        return TaskStatusSchema.model_validate(db_task_status)