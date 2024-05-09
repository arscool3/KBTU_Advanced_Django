from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI, Depends, HTTPException, Request, Response
import auth
import database as db
from models import Base
from database import engine
from core import route

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)


def get_db():
    try:
        session = db.session
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


entity_dependency = Annotated[dict, Depends(auth.get_current_entity)]
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {"message": "I'm alive"}


@app.get("/", status_code=status.HTTP_200_OK, tags=['check'])
async def entity(entity: entity_dependency, db: db_dependency):
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication failed!')
    return entity


@route(
    request_method=app.get,
    path='/restaurants',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url='http://localhost:8001',
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Restaurant',
    response_list=True,
    tags='customer'
)
async def get_restaurants(request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=app.get,
    path='/foods',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url='http://localhost:8001',
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Food',
    response_list=True,
    tags='customer'
)
async def get_foods(request: Request, response: Response, entity: entity_dependency):
    pass


@route(
    request_method=app.get,
    path='/restaurants/{_id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url='http://localhost:8001',
    authentication_required=True,
    post_processing_func=None,
    authentication_token_decoder='auth.decode_access_token',
    service_authorization_checker='auth.is_default_user',
    service_header_generator='auth.generate_request_header',
    response_model='schemas.Food',
    response_list=True,
    tags='customer'
)
async def restaurant_foods(_id: str, request: Request, response: Response, entity: entity_dependency):
    pass
