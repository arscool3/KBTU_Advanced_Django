import punq

from app.dependencies.director import DirectorCreateDependency
from app.dependencies.genre import GenreCreateDependency
from app.dependencies.movie import MovieCreateDependency
from app.dependencies.studio import StudioCreateDependency
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency
from utils.repository import AbcRepository


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())

    container.register(ListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    container.register(GenreCreateDependency)
    container.register(MovieCreateDependency)
    container.register(DirectorCreateDependency)
    container.register(StudioCreateDependency)

    return container