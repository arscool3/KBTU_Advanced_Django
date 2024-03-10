import database
import models
import target_handler

from fastapi import FastAPI

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(target_handler.router, prefix="/target", tags=["targets"])




