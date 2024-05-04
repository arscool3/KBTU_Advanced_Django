from fastapi import FastAPI
from task_comments.routers import router as task_comment_router
from projects.routers import router as project_router
from journal.routers import router as journal_router
from users.routers import router as user_router
from category.routers import router as category_router
from tasks.routers import router as task_router

app = FastAPI()


app.include_router(project_router)
app.include_router(journal_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(task_router)
app.include_router(task_comment_router)
