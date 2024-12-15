import punq as punq

from app.books.dependencies import BookCreateDependency
from app.members.dependencies import MemberCreateDependency
from app.utils.repository import AbcRepository
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.reservations.dependencies import ReservationCreateDependency
from app.authors.dependencies import AuthorCreateDependency
from app.publishers.dependencies import PublisherCreateDependency
from app.loans.dependencies import LoanCreateDependency


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())

    container.register(GetListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    container.register(BookCreateDependency)

    container.register(MemberCreateDependency)

    container.register(ReservationCreateDependency)

    container.register(AuthorCreateDependency)

    container.register(PublisherCreateDependency)

    container.register(LoanCreateDependency)

    return container
