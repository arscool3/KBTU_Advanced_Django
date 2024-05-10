from typing import Annotated
from fastapi import APIRouter, Request, Response, status, Depends, Query
import auth
from core import route
from config import CUSTOMER_SERVICE_URL
import schemas

router = APIRouter(
    tags=['customer'], prefix='/customer'
)

entity_dependency = Annotated[dict, Depends(auth.get_current_entity)]


@route(
    request_method=router.get,
    path='/restaurants',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Restaurant',
    response_list=True,
)
async def get_restaurants(request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.get,
    path='/foods',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Food',
    response_list=True,
)
async def get_foods(entity: entity_dependency, request: Request, response: Response):
    pass


@route(
    request_method=router.get,
    path='/restaurants/{_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Food',
    response_list=True,
)
async def restaurant_foods(_id: str, request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.post,
    path='/orders',
    status_code=status.HTTP_201_CREATED,
    payload_key='order',
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
)
async def create_order(order: schemas.CreateOrder, request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.get,
    path='/orders/{order_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.OrderDetail',
)
async def order_detail(order_id: str, request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.patch,
    path='/orders/{order_id}',
    status_code=status.HTTP_200_OK,
    payload_key='order',
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
)
async def create_order_item(order: schemas.CreateOrderItem, order_id: str,
                            request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.get,
    path='/orders/history/{customer_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.OrderDetail',
    response_list=True,

)
async def history_customer_orders(customer_id: str, request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=router.patch,
    path='/orders/buy_order/{order_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=CUSTOMER_SERVICE_URL,
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
)
async def change_order_status(request: Request, response: Response, entity: entity_dependency,
                              order_id: str, status_request: str = Query('PAID', enum=['PAID', 'DENY-CUSTOMER'])):
    pass
