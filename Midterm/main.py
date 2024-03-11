from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from category.models import Category
from category.schemas import CreateCategory
from database import get_db


app = FastAPI()


# @app.get("/category")
# async def get(db: Session = Depends(get_db)):
#     repo = CategoryRepo(session=db)
#     return repo.list()

@app.post("/category", response_model=CreateCategory)
async def create_category(category: CreateCategory, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# @app.post("/category")
# async def post(request_body: CreateCategory, db: Session = Depends(get_db)):
#     repo = CategoryRepo(session=db)
#     return repo.create(request_body)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
