from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request, status, Query
import auth
from core import route
from config import COURIER_SERVICE_URL

router = APIRouter(
    prefix='/courier',
    tags=['courier']
)

courier_dependency = Annotated[dict, Depends(auth.oauth2_bearer_courier)]


@route(
    request_method=router.patch,
    path='/couriers/status/{_id}',
    status_code=status.HTTP_200_OK,
    payload_key='menu_item',
    service_url=COURIER_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header'
)
async def update_courier_status(_id: str, courier: courier_dependency, request: Request, response: Response,
                                status: str = Query('CLOSE', enum=['CLOSE', 'OPEN'])):
    pass


@route(
    request_method=router.patch,
    path='/orders/{order_id}/{courier_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=COURIER_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header'
)
async def change_order_status(order_id: str, courier_id: str, request: Request, response: Response,
                              status_req: str = Query('DENY-COURIER', enum=
                              ['DENY-COURIER', 'ACCEPTED-COURIER', 'DELIVERED', 'IN-TRANSIT'])):
    pass


@route(
    request_method=router.get,
    path='/orders/{courier_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=COURIER_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.OrderDetail',
    response_list=True,
)
async def history_order_by_id(request: Request, response: Response, courier_id: str | None = None,
                              status_req: str = Query('READY', enum=['DENY-COURIER',
                                                                     'ACCEPTED-COURIER',
                                                                     'IN-TRANSIT',
                                                                     'DELIVERED'])):
    pass


@route(
    request_method=router.get,
    path='/orders/{order_id}/{courier_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=COURIER_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.CourierOrderDetail',
)
async def order_detail(order_id: str, courier_id: str, request: Request, response: Response):
    pass
