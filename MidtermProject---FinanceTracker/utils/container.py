import punq as punq

from accounts.dependencies import AccountCreateDependency
from utils.repository import AbcRepository
from utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from users.dependencies import UserCreateDependency


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())

    container.register(GetListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    container.register(UserCreateDependency)

    container.register(AccountCreateDependency)

    return container
