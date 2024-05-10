from typing import Annotated
from fastapi import APIRouter, Request, Response, status, Depends, Query
import auth
import schemas
from config import RESTAURANT_SERVICE_URL
from core import route

router = APIRouter(
    prefix='/restaurant',
    tags=['restaurant']
)

restaurant_dependency = Annotated[dict, Depends(auth.get_current_restaurant)]


@route(
    request_method=router.post,
    path='/restaurants/menu',
    status_code=status.HTTP_201_CREATED,
    payload_key='menu_item',
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
)
# restaurant: restaurant_dependency
async def create_menu_item(menu_item: schemas.CreateMenuItem, request: Request,
                           response: Response):
    pass


@route(
    request_method=router.patch,
    path='/restaurants/menu/{menu_item_id}',
    status_code=status.HTTP_200_OK,
    payload_key='menu_item',
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.MenuItem',
    response_list=False
)
async def update_menu_item(menu_item: schemas.UpdateMenuItem, menu_item_id: str,
                           request: Request, response: Response):
    pass


@route(
    request_method=router.patch,
    path='/restaurants/status/{restaurant_id}',
    status_code=status.HTTP_200_OK,
    payload_key='menu_item',
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header'
)
async def update_status_restaurant(restaurant_id: str, request: Request, response: Response,
                                   status_req: str = Query('CLOSE', enum=['CLOSE', 'OPEN'])):
    pass


@route(
    request_method=router.get,
    path='/orders/{order_id}/{restaurant_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.OrderDetail',
)
async def order_detail(order_id: str, restaurant_id: str, request: Request, response: Response):
    pass


@route(
    request_method=router.patch,
    path='/orders/{order_id}/{restaurant_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header'
)
async def change_status(order_id: str, restaurant_id: str, request: Request, response: Response,
                        status: str = Query('DENY-RESTAURANT',
                                            enum=['ACCEPTED-RESTAURANT', 'DENY-RESTAURANT', 'READY'])):
    pass


""


@route(
    request_method=router.get,
    path='/orders/{restaurant_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=RESTAURANT_SERVICE_URL,
    authentication_required=False,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.OrderDetail',
    response_list=True,
)
async def history_orders(restaurant_id: str, request: Request, response: Response,
                         status_req: str = Query('DENY', enum =
                         ['PENDING', 'DENY-COURIER', 'DENY-RESTAURANT',
                          'DENY-CUSTOMER', 'PAID', 'ACCEPTED-RESTAURANT',
                          'ACCEPTED-COURIER', 'READY', 'IN-TRANSIT', 'DELIVERED'])):
    pass
