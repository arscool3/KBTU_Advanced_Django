from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.members.repository import MemberRepo
from app.members.dependencies import MemberCreateDependency
from fastapi import APIRouter

router = APIRouter(prefix="/member", tags=["Members"])

router.add_api_route("/get_members", get_container(MemberRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_member", get_container(MemberRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_member", get_container(MemberRepo).resolve(MemberCreateDependency), methods=["POST"])

router.add_api_route("/delete_member", get_container(MemberRepo).resolve(DeleteDependency), methods=["DELETE"])

