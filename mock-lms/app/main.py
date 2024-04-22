from fastapi import FastAPI
from .api import user_controller, course_controller, comment_controller, lesson_controller, module_controller
from .database import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="LMS")

app.include_router(user_controller.router, prefix="/api/v1", tags=["users"])
app.include_router(course_controller.router, prefix="/api/v1", tags=["courses"])
app.include_router(comment_controller.router, prefix="/api/v1", tags=["comments"])
app.include_router(lesson_controller.router, prefix="/api/v1", tags=["lessons"])
app.include_router(module_controller.router, prefix="/api/v1", tags=["modules"])
