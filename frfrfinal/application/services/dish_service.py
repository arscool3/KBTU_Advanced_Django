from typing import Any

from fastapi import Depends

from application.cache.cache import RedisRepository
from application.db_app import schemas
from application.repositories.dish_repository import DishRepository
from application.services.menu_service import MenuService
from application.services.submenu_service import SubmenuService


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends()):
        self.dish_repository = dish_repository
        self.redis = RedisRepository()
        self.cache_name = 'dish_cache'
        self.menu_service = MenuService()
        self.submenu_service = SubmenuService()

    def set_cache(self, value: Any, dish_id: int | None = None, if_list: bool = False) -> Any:
        name = self.cache_name
        if if_list is True:
            return self.redis.set_cache(name=f'{name}', value=value, if_list=True)
        if dish_id:
            return self.redis.set_cache(name=f'{name}_{dish_id}', value=value)
        return self.redis.set_cache(name=name, value=value)

    def get_cache(self, dish_id: int | None = None) -> Any:
        name = self.cache_name
        if dish_id:
            return self.redis.get_cache(name=f'{name}_{dish_id}')
        return self.redis.get_cache(name=name)

    def delete_cache(self, dish_id: int | None = None) -> Any:
        name = self.cache_name
        if dish_id:
            self.redis.delete_cache(name=f'{name}_{dish_id}')
        self.redis.delete_cache('menu_cache')
        self.redis.delete_cache('submenu_cache')
        return self.redis.delete_cache(name=f'{name}')

    def update_dish_cache(self, menu_id: int, submenu_id: int, dish_id: int | None = None) -> Any:
        if dish_id:
            dish = self.dish_repository.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
            return self.set_cache(value=dish, dish_id=dish_id)
        dishes = self.dish_repository.get_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return self.set_cache(value=dishes, if_list=True)

    def get_dishes(self, menu_id: int, submenu_id: int) -> Any:
        dishes = self.dish_repository.get_dishes(menu_id=menu_id, submenu_id=submenu_id)
        get_cache = self.get_cache()
        if not get_cache:
            self.set_cache(value=dishes, if_list=True)
            return dishes
        return get_cache

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> Any:
        dish = self.dish_repository.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        get_cache = self.get_cache(dish_id=dish_id)
        if not get_cache:
            self.set_cache(value=dish, dish_id=dish_id)
            return dish
        return get_cache

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> Any:
        delete = self.dish_repository.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        self.delete_cache()
        self.delete_cache(dish_id=dish_id)
        self.submenu_service.delete_cache(submenu_id=submenu_id)
        self.menu_service.delete_cache(menu_id=menu_id)
        return delete

    def update_dish(self, dish_schemas: schemas.DishUpdate, menu_id: int,
                    submenu_id: int, dish_id: int) -> Any:
        update = self.dish_repository.update_dish(dish_schemas=dish_schemas,
                                                  menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        self.update_dish_cache(menu_id=menu_id, submenu_id=submenu_id)
        self.update_dish_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return update

    def create_dish(self, dish_schemas: schemas.DishCreate, menu_id: int, submenu_id: int) -> Any:
        create = self.dish_repository.create_dish(dish_schema=dish_schemas, menu_id=menu_id, submenu_id=submenu_id)
        self.delete_cache()
        self.submenu_service.delete_cache(submenu_id=submenu_id)
        self.menu_service.delete_cache(menu_id=menu_id)
        return create
