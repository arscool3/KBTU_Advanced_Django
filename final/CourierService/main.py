from copy import deepcopy
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from courier import router
import database as db

app = FastAPI()
app.include_router(router)


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


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {'message': "I'm alive"}


# TODO - Accept/Deny/Delivered change status
@app.patch("/orders/{order_id}/{courier_id}", tags=['orders'])
async def change_order_status(db: db_dependency, order_id: str, courier_id: str,
                              status_req: str = Query('DENY', enum=['DENY', 'ACCEPTED', 'DELIVERED'])):
    try:
        orders = db.execute(select(models.Order).filter(models.Order.courier_id == courier_id).
                            filter(models.Order.id == order_id)).scalars().all()
        if not orders:
            return {'message': 'order not found!'}
        orders[0].status = status_req
        return {'message': 'status is changed!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


# TODO - See history order by status
@app.get("/orders", tags=['orders'])
async def history_order_by_id(db: db_dependency, courier_id: str | None = None,
                              status_req: str = Query('READY',
                                                      enum=['PENDING', 'DENY', 'PAID', 'ACCEPTED', 'READY',
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
@app.get("/orders/{order_id}", tags=['orders'])
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
