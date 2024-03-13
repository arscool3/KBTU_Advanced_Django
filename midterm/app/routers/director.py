from fastapi import APIRouter

from app.dependencies.director import DirectorCreateDependency
from app.dependencies.genre import GenreCreateDependency
from app.repositories.director import DirectorRepo
from app.repositories.genre import GenreRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(
    prefix="/director",
    tags=["Directors"]
)

router.add_api_route("/", get_container(DirectorRepo).resolve(DirectorCreateDependency), methods=["POST"],
                     name="create director")
router.add_api_route("/", get_container(GenreRepo).resolve(ListDependency), methods=["GET"],
                     name="list_director")
router.add_api_route("/{id}", get_container(GenreRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_director")
router.add_api_route("/{id}", get_container(GenreRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_director")