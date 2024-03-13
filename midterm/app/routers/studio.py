from fastapi import APIRouter

from app.dependencies.genre import GenreCreateDependency
from app.dependencies.studio import StudioCreateDependency
from app.repositories.genre import GenreRepo
from app.repositories.studio import StudioRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(
    prefix="/studio",
    tags=["Studios"]
)

router.add_api_route("/", get_container(StudioRepo).resolve(StudioCreateDependency), methods=["POST"],
                     name="create studio")
router.add_api_route("/", get_container(StudioRepo).resolve(ListDependency), methods=["GET"],
                     name="list_studios")
router.add_api_route("/{id}", get_container(StudioRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_studio")
router.add_api_route("/{id}", get_container(StudioRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_studio")
