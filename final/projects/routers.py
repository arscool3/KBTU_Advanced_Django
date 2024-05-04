from fastapi import APIRouter, Depends

from projects.dependencies import ProjectCreateDependency, add_user_to_project_dep
from projects.repository import ProjectRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(prefix="/project", tags=["Projects"])


router.add_api_route(
    "/", get_container(ProjectRepo).resolve(ProjectCreateDependency),
    methods=["POST"], name="create_project",
)
router.add_api_route(
    "/", get_container(ProjectRepo).resolve(ListDependency),
    methods=["GET"], name="list_projects",
)
router.add_api_route(
    "/{id}", get_container(ProjectRepo).resolve(RetrieveDependency),
    methods=["GET"], name="retrieve_project",
)
router.add_api_route(
    "/{id}", get_container(ProjectRepo).resolve(DeleteDependency),
    methods=["DELETE"], name="delete_project",
)


@router.post("/add_user")
async def add_user_to_project(add_user_dep: str = Depends(add_user_to_project_dep)):
    return add_user_dep

