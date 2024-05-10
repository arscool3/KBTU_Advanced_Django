from copy import deepcopy
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from courier import router
import database as db

app = FastAPI()
main_router = APIRouter(prefix="/courier")
main_router.include_router(router)


def get_db():
    try:
        ss = db.session
        yield ss
        ss.commit()
    except Exception:
        raise
    finally:
        ss.close()


db_dependency = Annotated[Session, Depends(get_db)]


@main_router.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {'message': "I'm alive"}


# TODO - Accept/Deny/Delivered change status
@main_router.patch("/orders/{order_id}/{courier_id}", tags=['orders'])
async def change_order_status(db: db_dependency, order_id: str, courier_id: str,
                              status_req: str = Query('DENY-COURIER', enum=['DENY-COURIER', 'ACCEPTED-COURIER', 'DELIVERED', 'IN-TRANSIT'])):
    try:
        orders = db.execute(select(models.Order).filter(models.Order.courier_id == courier_id).
                            filter(models.Order.id == order_id)).scalars().all()
        if not orders:
            return {'message': 'order not found!'}
        if orders[0].status in ['READY', 'ACCEPTED-COURIER', 'IN-TRANSIT']:
            orders[0].status = status_req
            return {'message': 'status is changed!'}
        return {'message': 'You cant change status!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


# TODO - See history order by status
@main_router.get("/orders/{courier_id}", tags=['orders'])
async def history_order_by_id(db: db_dependency, courier_id: str | None = None,
                              status_req: str = Query('DELIVERED',
                                                      enum=['DENY-COURIER',
                                                            'ACCEPTED-COURIER',
                                                            'IN-TRANSIT',
                                                            'DELIVERED'])):
    try:
        orders = db.execute(select(models.Order).filter(models.Order.courier_id == courier_id)).scalars().all()
        res = [x for x in orders if x.status == status_req]
        if not res:
            return {'message': 'orders not found!'}
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


# TODO - Order detail
@main_router.get("/orders/{order_id}/{courier_id}", tags=['orders'])
async def order_detail(session: db_dependency, order_id: str, courier_id: str):
    try:
        orders = session.execute(select(models.Order).filter(models.Order.id == order_id).filter(models.Order.courier_id == courier_id)).scalars().all()
        if not orders:
            return {'message': f'order not found by id: {order_id}'}
        t = deepcopy(orders[0])
        t.status = str(t.status)
        validated_order = schemas.Order.model_validate(t)
        return validated_order
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'{e}')


app.include_router(main_router)
