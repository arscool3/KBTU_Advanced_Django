
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.loans.repository import LoanRepo
from app.loans.dependencies import LoanCreateDependency
from fastapi import APIRouter

router = APIRouter(prefix="/loan", tags=["Loans"])

router.add_api_route("/get_loans", get_container(LoanRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_loan", get_container(LoanRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_loan", get_container(LoanRepo).resolve(LoanCreateDependency), methods=["POST"])

router.add_api_route("/delete_loan", get_container(LoanRepo).resolve(DeleteDependency), methods=["DELETE"])

