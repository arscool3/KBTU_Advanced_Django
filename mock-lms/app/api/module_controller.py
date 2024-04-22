from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.schemas import ModuleCreate, Module
from ..models.models import Module as ModuleModel
from ..dependencies import get_db

router = APIRouter()


@router.post("/modules/", response_model=Module, status_code=status.HTTP_201_CREATED)
async def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    db_module = ModuleModel(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


@router.get("/modules/", response_model=List[Module])
def read_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    modules = db.query(ModuleModel).offset(skip).limit(limit).all()
    return modules


@router.get("/modules/{module_id}", response_model=Module)
def read_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.put("/modules/{module_id}", response_model=Module)
def update_module(module_id: int, module: ModuleCreate, db: Session = Depends(get_db)):
    db_module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    db_module.title = module.title
    db_module.description = module.description
    db.commit()
    return db_module


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    db.delete(module)
    db.commit()
    return {"ok": True}
