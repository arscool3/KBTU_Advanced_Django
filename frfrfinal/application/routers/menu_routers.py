from fastapi import APIRouter, Depends, HTTPException

from application.db_app import schemas
from application.services.menu_service import MenuService

router = APIRouter(prefix='/api/v1')


@router.post('/menus', response_model=schemas.Menu, status_code=201)
def create_menu(schema: schemas.MenuCreate, menu: MenuService = Depends()) -> schemas.Menu:
    return menu.create_menu(menu_schemas=schema)


@router.get('/menus', response_model=list[schemas.Menu])
def read_menus(menu: MenuService = Depends()) -> list[schemas.Menu]:
    return menu.get_menus()


@router.patch('/menus/{target_menu_id}', response_model=schemas.Menu)
def update_menus(target_menu_id: int, schema: schemas.MenuUpdate,
                 menu: MenuService = Depends()) -> HTTPException | schemas.Menu:
    return menu.update_menu(menu_schemas=schema, menu_id=target_menu_id)


@router.delete('/menus/{target_menu_id}', response_model=None)
def delete_menus(target_menu_id: int, menu: MenuService = Depends()) -> HTTPException | dict[str, str | bool]:
    return menu.delete_menu(menu_id=target_menu_id)


@router.get('/menus/{target_menu_id}', response_model=schemas.Menu)
def read_menu(target_menu_id: int, menu: MenuService = Depends()) -> HTTPException | schemas.Menu:
    return menu.get_menu(menu_id=target_menu_id)
