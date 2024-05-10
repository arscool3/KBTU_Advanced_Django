from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI, Depends, HTTPException, Request, Response
import auth
import database as db
from models import Base
from database import engine
import customer
import restaurant
import courier
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(restaurant.router)
app.include_router(courier.router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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
