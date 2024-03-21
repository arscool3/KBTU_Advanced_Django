
from fastapi import APIRouter
from users.repository import UserRepo
from users.dependencies import UserCreateDependency
from utils.container import get_container
from utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency


router = APIRouter(prefix="/user", tags=["Users"])

router.add_api_route("/get_users", get_container(UserRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_user_by_id", get_container(UserRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_user", get_container(UserRepo).resolve(UserCreateDependency), methods=["POST"])

router.add_api_route("/delete_user", get_container(UserRepo).resolve(DeleteDependency), methods=["DELETE"])



