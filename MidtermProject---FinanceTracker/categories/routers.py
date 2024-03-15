
from utils.container import get_container
from utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from categories.repository import CategoryRepo
from categories.dependencies import CategoryCreateDependency
from fastapi import APIRouter

router = APIRouter(prefix="/category", tags=["Categories"])

router.add_api_route("/get_categories", get_container(CategoryRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_category", get_container(CategoryRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_category", get_container(CategoryRepo).resolve(CategoryCreateDependency), methods=["POST"])

router.add_api_route("/delete_category", get_container(CategoryRepo).resolve(DeleteDependency), methods=["DELETE"])

