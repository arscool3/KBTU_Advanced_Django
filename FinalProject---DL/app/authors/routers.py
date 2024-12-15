from fastapi import APIRouter
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.authors.repository import AuthorRepo
from app.authors.dependencies import AuthorCreateDependency

router = APIRouter(prefix="/author", tags=["Authors"])

router.add_api_route("/get_authors", get_container(AuthorRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_author", get_container(AuthorRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_author", get_container(AuthorRepo).resolve(AuthorCreateDependency), methods=["POST"])

router.add_api_route("/delete_author", get_container(AuthorRepo).resolve(DeleteDependency), methods=["DELETE"])
