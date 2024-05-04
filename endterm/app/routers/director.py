from fastapi import APIRouter

from app.dependencies.director import DirectorCreateDependency
from app.dependencies.genre import GenreCreateDependency
from app.dramatiq_job.main import check_person_from_whitelist, check_director, result
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
router.add_api_route("/", get_container(DirectorRepo).resolve(ListDependency), methods=["GET"],
                     name="list_director")
router.add_api_route("/{id}", get_container(DirectorRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_director")
router.add_api_route("/{id}", get_container(DirectorRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_director")
router.add_api_route("/check_from_whitelist", check_director, methods=["POST"])
router.add_api_route("/result/{id}", result, methods=["GET"])