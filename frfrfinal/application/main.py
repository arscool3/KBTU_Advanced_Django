from fastapi import FastAPI

from application.db_app import models
from application.db_app.database import engine
from application.routers import dish_routers, menu_routers, submenu_routers

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(menu_routers.router)
app.include_router(submenu_routers.router)
app.include_router(dish_routers.router)
