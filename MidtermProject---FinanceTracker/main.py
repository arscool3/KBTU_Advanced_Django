from fastapi import FastAPI
from users.routers import router as user_router
from accounts.routers import router as account_router


app = FastAPI()

app.include_router(user_router)

app.include_router(account_router)



