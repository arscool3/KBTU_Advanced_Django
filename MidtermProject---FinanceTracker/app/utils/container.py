import punq as punq

from app.accounts.dependencies import AccountCreateDependency
from app.transactions.dependencies import TransactionCreateDependency
from app.utils.repository import AbcRepository
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.users.dependencies import UserCreateDependency
from app.budgets.dependencies import BudgetCreateDependency
from app.categories.dependencies import CategoryCreateDependency
from app.expenses.dependencies import ExpenseCreateDependency


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()

    container.register(AbcRepository, repository, instance=repository())

    container.register(GetListDependency)
    container.register(RetrieveDependency)
    container.register(DeleteDependency)

    container.register(UserCreateDependency)

    container.register(AccountCreateDependency)

    container.register(TransactionCreateDependency)

    container.register(CategoryCreateDependency)

    container.register(BudgetCreateDependency)

    container.register(ExpenseCreateDependency)

    return container
