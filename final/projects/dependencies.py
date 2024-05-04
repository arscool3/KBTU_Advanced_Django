from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from projects.repository import ProjectRepo
from projects.schemas import CreateProject, AddUserToProject
from utils.dependencies import BaseDependency


class ProjectCreateDependency(BaseDependency):

    def __call__(self, body: CreateProject, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)


def add_user_to_project_dep(instance: AddUserToProject, session: Session = Depends(get_db)):
    project_repo = ProjectRepo()
    project_repo.session = session
    return project_repo.add_user_to_project(instance)
