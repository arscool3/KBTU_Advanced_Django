from fastapi import APIRouter
from utils.container import get_container
from utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from scripts.accounts.repository import AccountRepo
from scripts.accounts.dependencies import AccountCreateDependency

router = APIRouter(prefix="/account", tags=["Accounts"])

router.add_api_route("/get_accounts", get_container(AccountRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_account", get_container(AccountRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_account", get_container(AccountRepo).resolve(AccountCreateDependency), methods=["POST"])

router.add_api_route("/delete_account", get_container(AccountRepo).resolve(DeleteDependency), methods=["DELETE"])
