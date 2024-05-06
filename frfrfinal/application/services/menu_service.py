from typing import Any

from fastapi import Depends

from application.cache.cache import RedisRepository
from application.db_app import schemas
from application.repositories.menu_repository import MenuRepository


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends()):
        self.menu_repository = menu_repository
        self.redis = RedisRepository()
        self.cache_name = 'menu_cache'

    def set_cache(self, value: Any, menu_id: int | None = None, if_list: bool = False) -> Any:
        name = self.cache_name
        if if_list is True:
            return self.redis.set_cache(name=f'{name}', value=value, if_list=True)
        if menu_id:
            return self.redis.set_cache(name=f'{name}_{menu_id}', value=value)
        return self.redis.set_cache(name=name, value=value)

    def get_cache(self, menu_id: int | None = None) -> Any:
        name = self.cache_name
        if menu_id:
            return self.redis.get_cache(name=f'{name}_{menu_id}')
        return self.redis.get_cache(name=name)

    def delete_cache(self, menu_id: int | None = None) -> Any:
        name = self.cache_name
        if menu_id:
            return self.redis.delete_cache(name=f'{name}_{menu_id}')
        self.redis.delete_cache(name='submenu_cache')
        self.redis.delete_cache(name='dish_cache')
        return self.redis.delete_cache(name=f'{name}')

    def update_menu_cache(self, menu_id: int | None = None) -> Any:
        if menu_id:
            menu = self.menu_repository.get_menu(menu_id=menu_id)
            return self.set_cache(value=menu, menu_id=menu_id)
        menus = self.menu_repository.get_menus()
        return self.set_cache(value=menus, if_list=True)

    def get_menus(self) -> Any:
        menus = self.menu_repository.get_menus()
        get_cache = self.get_cache()
        if not get_cache:
            self.set_cache(value=menus, if_list=True)
            return menus
        return get_cache

    def get_menu(self, menu_id: int) -> Any:
        menu = self.menu_repository.get_menu(menu_id=menu_id)
        get_cache = self.get_cache(menu_id=menu_id)
        if not get_cache:
            self.set_cache(value=menu, menu_id=menu_id)
            return menu
        return get_cache

    def delete_menu(self, menu_id: int) -> Any:
        delete = self.menu_repository.delete_menu(menu_id=menu_id)
        self.delete_cache()
        self.delete_cache(menu_id=menu_id)
        return delete

    def update_menu(self, menu_schemas: schemas.MenuUpdate, menu_id: int) -> Any:
        update = self.menu_repository.update_menu(menu_schemas=menu_schemas, menu_id=menu_id)
        self.update_menu_cache()
        self.update_menu_cache(menu_id=menu_id)
        return update

    def create_menu(self, menu_schemas: schemas.MenuCreate) -> Any:
        create = self.menu_repository.create_menu(menu_schemas=menu_schemas)
        self.delete_cache()
        return create
