from typing import Any, Sequence

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row, distinct, func, select
from sqlalchemy.orm import Session

from application.db_app import schemas
from application.db_app.database import connect_db
from application.db_app.models import Dish, Menu, Submenu
from application.repositories.menu_repository import MenuRepository


class SubmenuRepository:

    def __init__(self, session: Session = Depends(connect_db)):
        self.db: Session = session
        self.menu = Menu
        self.submenu = Submenu
        self.dish = Dish
        self.menu_repository = MenuRepository(session=session)

    def get_submenus(self, menu_id: int) -> HTTPException | Sequence[Row[tuple[Any]]] | None:
        menu = self.menu_repository.get_menu(menu_id=menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail='submenu not found')
        result = self.db.execute(
            select(
                self.submenu.id,
                self.submenu.menu_id,
                self.submenu.title,
                self.submenu.description,
                func.count(distinct(self.dish.id)).label('dishes_count'),
            ).filter(self.submenu.menu_id == menu_id)
            .outerjoin(self.dish, self.submenu.id == self.dish.submenu_id)
            .group_by(self.submenu.id)
        )
        return result.all()

    def get_submenu(self, menu_id: int, submenu_id: int) -> HTTPException | Row[tuple[Any]] | None:
        result = self.db.execute(
            select(
                self.submenu.id,
                self.submenu.menu_id,
                self.submenu.title,
                self.submenu.description,
                func.count(distinct(self.dish.id)).label('dishes_count'),
            ).filter(self.submenu.menu_id == menu_id, self.submenu.id == submenu_id)
            .outerjoin(self.dish, self.submenu.id == self.dish.submenu_id)
            .group_by(self.submenu.id)
        ).first()
        if not result:
            raise HTTPException(status_code=404, detail='submenu not found')
        return result

    def create_submenu(self, submenu_schemas: schemas.SubmenuCreate, menu_id: int) -> HTTPException | Row[tuple[Any]]:
        menu = self.menu_repository.get_menu(menu_id=menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        db_submenu = self.submenu(**submenu_schemas.model_dump(), menu_id=menu_id)
        self.db.add(db_submenu)
        self.db.commit()
        self.db.refresh(db_submenu)
        submenu_id = jsonable_encoder(db_submenu)['id']
        return self.get_submenu(menu_id=menu_id, submenu_id=submenu_id)

    def update_submenu(self, submenu_schemas: schemas.SubmenuUpdate, menu_id: int,
                       submenu_id: int) -> HTTPException | Row[tuple[Any]]:
        submenu = self.db.query(self.submenu).filter(self.submenu.menu_id == menu_id,
                                                     self.submenu.id == submenu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='menu id or submenu id not found')
        new_data = submenu_schemas.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(submenu, key, value)
        self.db.add(submenu)
        self.db.commit()
        self.db.refresh(submenu)
        return self.get_submenu(menu_id=menu_id, submenu_id=submenu_id)

    def delete_submenu(self, menu_id: int, submenu_id: int) -> HTTPException | dict[str, str | bool]:
        result = self.db.query(self.submenu).filter(self.submenu.menu_id == menu_id,
                                                    self.submenu.id == submenu_id).first()
        if not result:
            raise HTTPException(status_code=404, detail='menu id or submenu id not found')
        self.db.delete(result)
        self.db.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
