
from fastapi import APIRouter
from app.reservations.repository import ReservationRepo
from app.reservations.dependencies import ReservationCreateDependency
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency


router = APIRouter(prefix="/reservation", tags=["Reservations"])

router.add_api_route("/get_reservations", get_container(ReservationRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_reservation", get_container(ReservationRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_reservation", get_container(ReservationRepo).resolve(ReservationCreateDependency), methods=["POST"])

router.add_api_route("/delete_reservation", get_container(ReservationRepo).resolve(DeleteDependency), methods=["DELETE"])



