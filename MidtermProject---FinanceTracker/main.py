from fastapi import FastAPI
from users.routers import router as user_router
from accounts.routers import router as account_router
from transactions.routers import router as transaction_router
from categories.routers import router as category_router
from budgets.routers import router as budget_router


app = FastAPI()

app.include_router(user_router)

app.include_router(account_router)

app.include_router(transaction_router)

app.include_router(category_router)

app.include_router(budget_router)



