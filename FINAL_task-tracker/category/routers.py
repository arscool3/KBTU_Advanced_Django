from fastapi import APIRouter

from category.dependencies import CategoryCreateDependency
from category.repository import CategoryRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(prefix="/category", tags=["Categories"])


router.add_api_route("/", get_container(CategoryRepo).resolve(CategoryCreateDependency), methods=["POST"],
                     name="create_category")
router.add_api_route("/", get_container(CategoryRepo).resolve(ListDependency), methods=["GET"],
                     name="list_categories")
router.add_api_route("/{id}", get_container(CategoryRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_category")
router.add_api_route("/{id}", get_container(CategoryRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_category")
