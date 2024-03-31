from fastapi import FastAPI
from app.users.routers import router as user_router
from app.accounts.routers import router as account_router
from app.transactions.routers import router as transaction_router
from app.categories.routers import router as category_router
from app.budgets.routers import router as budget_router
from app.expenses.routers import router as expense_router


app = FastAPI()

app.include_router(user_router)

app.include_router(account_router)

app.include_router(transaction_router)

app.include_router(category_router)

app.include_router(budget_router)

app.include_router(expense_router)


