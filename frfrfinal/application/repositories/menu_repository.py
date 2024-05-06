from typing import Any, Sequence

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row, distinct, func, select
from sqlalchemy.orm import Session

from application.db_app import schemas
from application.db_app.database import connect_db
from application.db_app.models import Dish, Menu, Submenu


class MenuRepository:

    def __init__(self, session: Session = Depends(connect_db)):
        self.db: Session = session
        self.menu = Menu
        self.submenu = Submenu
        self.dish = Dish

    def get_menus(self) -> Sequence[Row[tuple[Any]]] | None:
        result = self.db.execute(
            select(
                self.menu.id,
                self.menu.title,
                self.menu.description,
                func.count(distinct(self.submenu.id)).label('submenus_count'),
                func.count(distinct(self.dish.id)).label('dishes_count'),
            )
            .outerjoin(self.submenu, self.menu.id == self.submenu.menu_id)
            .outerjoin(self.dish, self.submenu.id == self.dish.submenu_id)
            .group_by(self.menu.id)
        )
        return result.all()

    def get_menu(self, menu_id: int) -> HTTPException | Row[tuple[Any]] | None:
        result = self.db.execute(
            select(
                self.menu.id,
                self.menu.title,
                self.menu.description,
                func.count(distinct(self.submenu.id)).label('submenus_count'),
                func.count(distinct(self.dish.id)).label('dishes_count'),
            ).filter(self.menu.id == menu_id)
            .outerjoin(self.submenu, self.menu.id == self.submenu.menu_id)
            .outerjoin(self.dish, self.submenu.id == self.dish.submenu_id)
            .group_by(self.menu.id)
        ).first()
        if not result:
            raise HTTPException(status_code=404, detail='menu not found')
        return result

    def delete_menu(self, menu_id: int) -> HTTPException | dict[str, str | bool]:
        delete = self.db.query(self.menu).filter(self.menu.id == menu_id).first()
        if not delete:
            raise HTTPException(status_code=404, detail='menu not found')
        self.db.delete(delete)
        self.db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}

    def update_menu(self, menu_schemas: schemas.MenuUpdate, menu_id: int) -> HTTPException | Row[tuple[Any]]:
        menu = self.db.query(self.menu).filter(self.menu.id == menu_id).first()
        new_data = menu_schemas.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(menu, key, value)
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return self.get_menu(menu_id=menu_id)

    def create_menu(self, menu_schemas: schemas.MenuCreate) -> Row[tuple[Any]]:
        db_menu = self.menu(**menu_schemas.model_dump())
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        menu_id = jsonable_encoder(db_menu)['id']
        return self.get_menu(menu_id)
