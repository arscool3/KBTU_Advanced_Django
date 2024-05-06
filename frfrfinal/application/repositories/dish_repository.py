from typing import Any

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row, select
from sqlalchemy.orm import Session

from application.db_app import schemas
from application.db_app.database import connect_db
from application.db_app.models import Dish, Menu, Submenu
from application.repositories.submenu_repository import SubmenuRepository


class DishRepository:

    def __init__(self, session: Session = Depends(connect_db)):
        self.db: Session = session
        self.menu = Menu
        self.submenu = Submenu
        self.dish = Dish
        self.submenu_repository = SubmenuRepository(session=session)

    def get_dishes(self, menu_id: int, submenu_id: int) -> Any | None:
        result = self.db.execute(
            select(
                self.dish.id,
                self.dish.submenu_id,
                self.dish.title,
                self.dish.description,
                self.dish.price
            ).filter(self.dish.menu_id == menu_id, self.dish.submenu_id == submenu_id)
            .group_by(self.dish.id)
        )
        return result.all()

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> HTTPException | Row[tuple] | None:
        result = self.db.execute(
            select(
                self.dish.id,
                self.dish.submenu_id,
                self.dish.title,
                self.dish.description,
                self.dish.price
            ).filter(self.dish.menu_id == menu_id, self.dish.submenu_id == submenu_id, self.dish.id == dish_id)
        ).first()
        if not result:
            raise HTTPException(status_code=404, detail='dish not found')
        return result

    def create_dish(self, dish_schema: schemas.DishCreate, menu_id: int,
                    submenu_id: int) -> HTTPException | Row[tuple[Any]]:
        self.submenu_repository.get_submenu(menu_id=menu_id, submenu_id=submenu_id)
        db_dish = self.dish(**dish_schema.model_dump(), menu_id=menu_id, submenu_id=submenu_id)
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        dish_id = jsonable_encoder(db_dish)['id']
        return self.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

    def update_dish(self, dish_schemas: schemas.DishUpdate, menu_id: int,
                    submenu_id: int, dish_id: int) -> HTTPException | Row[tuple[Any]]:
        dish = self.db.query(self.dish).filter(self.dish.menu_id == menu_id,
                                               self.dish.submenu_id == submenu_id,
                                               self.dish.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail='menu id, submenu id or dish id not found')
        new_data = dish_schemas.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(dish, key, value)
        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)
        return self.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> HTTPException | dict[str, str | bool]:
        result = self.db.query(self.dish).filter(self.dish.menu_id == menu_id,
                                                 self.dish.submenu_id == submenu_id,
                                                 self.dish.id == dish_id).first()
        if not result:
            raise HTTPException(status_code=404, detail='menu id, submenu id or dish id not found')
        self.db.delete(result)
        self.db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
