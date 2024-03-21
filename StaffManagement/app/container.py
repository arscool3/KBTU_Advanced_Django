import punq
from fastapi import Depends

from app.database import get_db
from app.repository import AbcRepository
from app.dependencies import GetListDependency, DepartmentCreateDependency, \
    EmployeeCreateDependency, TaskCreateDependency, ScheduleCreateDependency


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository(session=Depends(get_db)))

    container.register(GetListDependency)
    container.register(DepartmentCreateDependency)
    container.register(EmployeeCreateDependency)
    container.register(TaskCreateDependency)
    container.register(ScheduleCreateDependency)

    return container
