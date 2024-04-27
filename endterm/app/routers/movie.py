from fastapi import APIRouter

from app.dependencies.genre import GenreCreateDependency
from app.dependencies.movie import MovieCreateDependency
from app.repositories.genre import GenreRepo
from app.repositories.movie import MovieRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(
    prefix="/movie",
    tags=["Movies"]
)

router.add_api_route("/", get_container(MovieRepo).resolve(MovieCreateDependency), methods=["POST"],
                     name="create movies")
router.add_api_route("/", get_container(MovieRepo).resolve(ListDependency), methods=["GET"],
                     name="list_movies")
router.add_api_route("/{id}", get_container(MovieRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_movies")
router.add_api_route("/{id}", get_container(MovieRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_movies")