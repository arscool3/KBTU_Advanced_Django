from fastapi import APIRouter
from starlette.websockets import WebSocket

from users.dependencies import UserCreateDependency
from users.repository import UserRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency
from celery_worker import send_report_on_email

router = APIRouter(prefix="/user", tags=["Users"])


router.add_api_route(
    "/", get_container(UserRepo).resolve(UserCreateDependency),
    methods=["POST"], name="create_user",
)
router.add_api_route(
    "/", get_container(UserRepo).resolve(ListDependency),
    methods=["GET"], name="list_users",
)
router.add_api_route(
    "/{id}", get_container(UserRepo).resolve(RetrieveDependency),
    methods=["GET"], name="retrieve_user",
)
router.add_api_route(
    "/{id}", get_container(UserRepo).resolve(DeleteDependency),
    methods=["DELETE"], name="delete_user",
)


@router.post("/report")
async def create_report(user_id: int):
    send_report_on_email.delay(user_id=user_id)
    return """Report will be sent on your email"""
