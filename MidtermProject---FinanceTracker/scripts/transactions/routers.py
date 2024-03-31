from utils.container import get_container
from utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from scripts.transactions.repository import TransactionRepo
from scripts.transactions.dependencies import TransactionCreateDependency
from fastapi import APIRouter

router = APIRouter(prefix="/transaction", tags=["Transactions"])

router.add_api_route("/get_transactions", get_container(TransactionRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_transaction", get_container(TransactionRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_transaction", get_container(TransactionRepo).resolve(TransactionCreateDependency), methods=["POST"])

router.add_api_route("/delete_transaction", get_container(TransactionRepo).resolve(DeleteDependency), methods=["DELETE"])

