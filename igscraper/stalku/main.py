import database
import models
import target_handler
import follow_handler
from fastapi import FastAPI

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(target_handler.router, prefix="/target", tags=["targets"])
app.include_router(follow_handler.router, prefix="/follow", tags=["follows"])



