from fastapi import APIRouter
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.budgets.repository import BudgetRepo
from app.budgets.dependencies import BudgetCreateDependency

router = APIRouter(prefix="/budget", tags=["Budgets"])

router.add_api_route("/get_budgets", get_container(BudgetRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_bedget", get_container(BudgetRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_budget", get_container(BudgetRepo).resolve(BudgetCreateDependency), methods=["POST"])

router.add_api_route("/delete_budget", get_container(BudgetRepo).resolve(DeleteDependency), methods=["DELETE"])
