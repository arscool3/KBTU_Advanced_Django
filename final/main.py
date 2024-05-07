from fastapi import FastAPI

import auth

app = FastAPI()

app.include_router(auth.router)
