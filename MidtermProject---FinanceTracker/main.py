from fastapi import FastAPI
from scripts.users.routers import router as user_router
from scripts.accounts.routers import router as account_router
from scripts.transactions.routers import router as transaction_router
from scripts.categories.routers import router as category_router
from scripts.budgets.routers import router as budget_router
from scripts.expenses.routers import router as expense_router


app = FastAPI()

app.include_router(user_router)

app.include_router(account_router)

app.include_router(transaction_router)

app.include_router(category_router)

app.include_router(budget_router)

app.include_router(expense_router)


