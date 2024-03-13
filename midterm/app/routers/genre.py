from fastapi import APIRouter

from app.dependencies.genre import GenreCreateDependency
from app.repositories.genre import GenreRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(
    prefix="/genre",
    tags=["Genres"]
)

router.add_api_route("/", get_container(GenreRepo).resolve(GenreCreateDependency), methods=["POST"],
                     name="create genre")
router.add_api_route("/", get_container(GenreRepo).resolve(ListDependency), methods=["GET"],
                     name="list_genres")
router.add_api_route("/{id}", get_container(GenreRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_genres")
router.add_api_route("/{id}", get_container(GenreRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_genres")