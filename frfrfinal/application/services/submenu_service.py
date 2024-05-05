from typing import Any

from fastapi import Depends

from application.cache.cache import RedisRepository
from application.db_app import schemas
from application.repositories.submenu_repository import SubmenuRepository
from application.services.menu_service import MenuService


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends()):
        self.submenu_repository = submenu_repository
        self.redis = RedisRepository()
        self.cache_name = 'submenu_cache'
        self.menu_service = MenuService()

    def set_cache(self, value: Any, submenu_id: int | None = None, if_list: bool = False) -> Any:
        name = self.cache_name
        if if_list is True:
            return self.redis.set_cache(name=f'{name}', value=value, if_list=True)
        if submenu_id:
            return self.redis.set_cache(name=f'{name}_{submenu_id}', value=value)
        return self.redis.set_cache(name=name, value=value)

    def get_cache(self, submenu_id: int | None = None) -> Any:
        name = self.cache_name
        if submenu_id:
            return self.redis.get_cache(name=f'{name}_{submenu_id}')
        return self.redis.get_cache(name=name)

    def delete_cache(self, submenu_id: int | None = None) -> Any:
        name = self.cache_name
        if submenu_id:
            self.redis.delete_cache(name=f'{name}_{submenu_id}')
        self.redis.delete_cache(name='menu_cache')
        self.redis.delete_cache(name='dish_cache')
        return self.redis.delete_cache(name=f'{name}')

    def update_submenu_cache(self, menu_id: int, submenu_id: int | None = None) -> Any:
        if submenu_id:
            submenu = self.submenu_repository.get_submenu(menu_id=menu_id, submenu_id=submenu_id)
            return self.set_cache(value=submenu, submenu_id=submenu_id)
        submenus = self.submenu_repository.get_submenus(menu_id=menu_id)
        return self.set_cache(value=submenus, if_list=True)

    def get_submenus(self, menu_id: int) -> Any:
        submenus = self.submenu_repository.get_submenus(menu_id=menu_id)
        get_cache = self.get_cache()
        if not get_cache:
            self.set_cache(value=submenus, if_list=True)
            return submenus
        return get_cache

    def get_submenu(self, menu_id: int, submenu_id: int) -> Any:
        submenu = self.submenu_repository.get_submenu(menu_id=menu_id, submenu_id=submenu_id)
        get_cache = self.get_cache(submenu_id=submenu_id)
        if not get_cache:
            self.set_cache(value=submenu, submenu_id=submenu_id)
            return submenu
        return get_cache

    def delete_submenu(self, menu_id: int, submenu_id: int) -> Any:
        delete = self.submenu_repository.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
        self.delete_cache()
        self.delete_cache(submenu_id=submenu_id)
        self.menu_service.delete_cache(menu_id=menu_id)
        return delete

    def update_submenu(self, submenu_schemas: schemas.SubmenuUpdate, menu_id: int, submenu_id: int) -> Any:
        update = self.submenu_repository.update_submenu(submenu_schemas=submenu_schemas,
                                                        menu_id=menu_id, submenu_id=submenu_id)
        self.update_submenu_cache(menu_id=menu_id)
        self.update_submenu_cache(menu_id=menu_id, submenu_id=submenu_id)
        return update

    def create_submenu(self, submenu_schemas: schemas.SubmenuCreate, menu_id: int) -> Any:
        create = self.submenu_repository.create_submenu(submenu_schemas=submenu_schemas, menu_id=menu_id)
        self.delete_cache()
        self.menu_service.delete_cache(menu_id=menu_id)
        return create
