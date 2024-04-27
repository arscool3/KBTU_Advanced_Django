import punq
from fastapi import Depends
from sqlalchemy.orm import Session

from category.dependencies import CategoryCreateDependency
from database import get_db, session
from projects.dependencies import ProjectCreateDependency
from task_comments.dependencies import TaskCommentCreateDependency
from tasks.dependencies import TaskCreateDependency
from users.dependencies import UserCreateDependency
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency
from utils.repository import AbcRepository


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())

    container.register(ListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    # register create deps
    container.register(CategoryCreateDependency)
    container.register(ProjectCreateDependency)
    container.register(TaskCommentCreateDependency)
    container.register(TaskCreateDependency)
    container.register(UserCreateDependency)

    return container
